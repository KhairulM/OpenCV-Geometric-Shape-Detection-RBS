""" Untuk menjalankan program harus install OpenCV 'pip install opencv-python' """

import cv2 as cv
import numpy as np
from sys import argv

def normalizePoint(coord, height, width):
    newX = (coord[0]*-1) + width//2
    newY = (coord[1]*-1) + height//2

    return np.array([newX, newY])

def processImage(imgfilepath, debug=False):
    """ Preparing the image """
    orgImg = cv.imread(imgfilepath)
    bwImg = cv.cvtColor(orgImg, cv.COLOR_BGR2GRAY)
    blurredImg = cv.GaussianBlur(bwImg, (5, 5), 0)
    ret, threshImg = cv.threshold(blurredImg, 200, 255, cv.THRESH_OTSU)
    halfImgHeight = orgImg.shape[:1][0]//2

    height, width = orgImg.shape[:2]
    cv.namedWindow("Edges", cv.WINDOW_AUTOSIZE)
    shapes = []
    result = dict()
    result['nbShapes'] = 0

    """ Finding edges """
    edgeImg = cv.Canny(threshImg, 30, 200)
    if debug:
        cv.imshow("Edges", edgeImg)
        cv.waitKey(0)

    """ Finding contours """
    contours, hierarchy = cv.findContours(edgeImg, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    """ Ambil contour mulai dari kedua, yang pertama biasanya contour border gambarnya (persegi) """
    for i in range(1, len(contours), 2):
        cnt = contours[i]

        """ Approksimasi titik2nya dengan Douglas-Peucker Algorithm """
        epPercent = 0.07 #10%
        epsilon = epPercent*cv.arcLength(cnt, True) #Sebetulnya ini bebas sih mau berapa epsilonnya, dikali arc length supaya bisa scale dengan image yang kecil maupun yang besar
        approx = cv.approxPolyDP(cnt, epsilon, True) #Berisi posisi simpul shape yang mau dideteksi
        
        """ Drawing contours """
        contImg = np.zeros((height, width, 3), np.uint8)
        cv.drawContours(contImg, contours, i, (0, 255, 255), 2)

        """ Menghitung sudut2nya """
        angles = []
        sides = []
        nbPoint = len(approx)
        calArr = [point for point in approx]
        calArr.append(approx[0])
        calArr.append(approx[1])
        for count in range(nbPoint):
            a = normalizePoint(calArr[count][0], height, width)
            b = normalizePoint(calArr[count+1][0], height, width)
            c = normalizePoint(calArr[count+2][0], height, width)

            ba = a - b
            bc = c - b

            angle = np.arccos(np.dot(ba, bc)/(np.linalg.norm(ba)*np.linalg.norm(bc)))
            angles.append(np.degrees(angle))

            """ Menghitung panjang """
            sides.append(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5)


        shape = dict()
        shape['vertices'] = nbPoint
        shape['angles'] = angles
        shape['sides'] = sides

        shapes.append(shape)
        result['nbShapes'] += 1
        
        if debug:
            print(shape)
            cv.imshow("Contour image " + str(i), contImg)
            cv.waitKey(0)

    result['shapes'] = shapes
    return result

if __name__ == "__main__":
    processImage(argv[1], True)