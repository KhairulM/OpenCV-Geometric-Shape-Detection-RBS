from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
import PIL.Image

#Create window
window = Tk()
window.geometry('1024x800')
window.title("Geometric Shape Detection using OpenCV")

#Functions
def openImage():
    file = filedialog.askopenfilename(filetypes = (("JPG/JPEG Pictures","*.jpg"),("all files","*.*")))  
    PILimage = PIL.Image.open(file)
    width, height = PILimage.size
    PILimage = PILimage.resize((height//300*width, 300), PIL.Image.ANTIALIAS)
    TKimage = PIL.Image.PhotoImage(PILimage)  
    srcImage.configure(image = TKimage)
    srcImage.image = TKimage 

    # photo=ImageTk.PhotoImage(img)
    # cv = Canvas()
    # cv.pack(side='top', fill='both', expand='yes')
    # cv.create_image(50, 50, image=photo, anchor='nw')  
    # srcImg = ImageTk.PhotoImage(Image.open(file))
    # srcImage.configure(image=srcImg, width=30, height=30)

# img=Image.open("Path to your image")
# photo=ImageTk.PhotoImage(img)
# cv = tk.Canvas()
# cv.pack(side='top', fill='both', expand='yes')
# cv.create_image(50, 50, image=photo, anchor='nw')

#Components
topPlaceholder = Label(window, width=1000, height=20, relief="sunken")
topPlaceholder.grid(column=0, row=0)

srcImageTitle = Label(topPlaceholder, text="Source Image", font=("Arial"), width = 40, padx=10)
srcImageTitle.grid(column=0, row=0)

detectionImageTitle = Label(topPlaceholder, text="Detection Image", font=("Arial"), width = 40)
detectionImageTitle.grid(column=1, row=0)

srcImage = Label(topPlaceholder, text="Place Image Here", font=("Arial"), borderwidth=2, relief="sunken", width=40, height=17)
srcImage.grid(column=0, row=1)

detectionImage = Label(topPlaceholder, text="Place Image Here", font=("Arial"), borderwidth=2, relief="sunken", width=40, height=17)
detectionImage.grid(column=1, row=1)

buttonPlaceholder = Label(topPlaceholder, width=150, height=20, relief="sunken")
buttonPlaceholder.grid(column=3, row=1)

openImgBtn = Button(buttonPlaceholder, text="Click Me", command=openImage, width=15)
openImgBtn.grid(column=0, row=0)

xImgBtn = Button(buttonPlaceholder, text="Click X", command=openImage, width=15)
xImgBtn.grid(column=0, row=1)

yImgBtn = Button(buttonPlaceholder, text="Click Y", command=openImage, width=15)
yImgBtn.grid(column=0, row=2)

zImgBtn = Button(buttonPlaceholder, text="Click Z", command=openImage, width=15)
zImgBtn.grid(column=0, row=3)

bottomPlaceholder = Label(window, width=1000, height=20, relief="sunken")
bottomPlaceholder.grid(column=0, row=1)

detectionResultTitle = Label(bottomPlaceholder, text="Detection Result", font=("Arial"), width = 20)
detectionResultTitle.grid(column=0, row=2)

matchedFactTitle = Label(bottomPlaceholder, text="Matched Facts", font=("Arial"), width = 20)
matchedFactTitle.grid(column=1, row=2)

hitRulesTitle = Label(bottomPlaceholder, text="Hit Rules", font=("Arial"), width = 20)
hitRulesTitle.grid(column=2, row=2)

detectionResult = Label(bottomPlaceholder, font=("Arial"), borderwidth=2, relief="sunken", width=35, height=15)
detectionResult.grid(column=0, row=3)

matchedFact = Label(bottomPlaceholder, font=("Arial"), borderwidth=2, relief="sunken", width=35, height=15)
matchedFact.grid(column=1, row=3)

hitRules = Label(bottomPlaceholder, font=("Arial"), borderwidth=2, relief="sunken", width=35, height=15)
hitRules.grid(column=2, row=3)

window.mainloop()


# txt = Entry(window,width=10)
# txt.grid(column=1, row=0)
# def clicked():
#     res = "Welcome to " + txt.get()
#     lbl.configure(text= res)
# btn = Button(window, text="Click Me", command=clicked)
# btn.grid(column=0, row=1)
