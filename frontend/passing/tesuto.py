from tkinter import *
#from playsound import playsound
from random import sample
from PIL import ImageTk
import PIL.Image
#from AppKit import NSScreen
from tkinter import messagebox
import os
from tkinter import filedialog
from tkinter import ttk
from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.filedialog import askopenfile 
from api import *

width = 1080
height = 720
class Deck:
    def __init__(self, master):
        self.source_file = ''
        self.source_img = Label(master, text='')
        self.det_img = Label(master, text='')
        # deckimg = PhotoImage(file = os.path.dirname(os.path.abspath('tesuto.py')) + '/purple_back.png')
        # self.source_img.configure(image = deckimg)
        # self.source_img.image = deckimg

        #SOURCE IMAGE
        im = PIL.Image.open("blankcard.jpg")
        width, height = im.size
        im = im.resize((height//300*width, 300), PIL.Image.ANTIALIAS)
        photo=ImageTk.PhotoImage(im)  
        self.source_img.configure(image = photo)
        self.source_img.image = photo 

        #DETECTION IMAGE
        im = PIL.Image.open("blankcard.jpg")
        width, height = im.size
        im = im.resize((height//300*width, 300), PIL.Image.ANTIALIAS)
        photo=ImageTk.PhotoImage(im)  
        self.det_img.configure(image = photo)
        self.det_img.image = photo 
        
        
        # Konfigurasi button: text, ukuran, command yang dijalankan saat pencet, padding
        self.img_button = Button(master, text="Open Image", font=("Comic Sans MS",10), command=self.img_button, padx=34, pady=3)
        self.rule_edit_button = Button(master, text="Open Rule Editor",font=("Comic Sans MS",10),command=lambda: self.rule_edit(master), padx=11, pady=3)
        self.rules_button = Button(master, text="Show Rules",font=("Comic Sans MS",10),command=lambda: self.rules(master), padx=38, pady=3)
        self.facts_button = Button(master, text="Show Facts",font=("Comic Sans MS",10),command=lambda: self.facts(master), padx=37, pady=3)
        self.exite_button = Button(master, text=" Exit ",font=("Comic Sans MS",10),command=self.exite, padx=18, pady=3)

        # Konfigurasi label (tulisan di atas gambar)
        self.labelSouImage = Label(master, text="Source Image", font=("Comic Sans MS",18))
        self.labelDestImage = Label(master, text="Detection Image", font=("Comic Sans MS",18))
        self.labelDetection = Label(master, text="Detection Result", font=("Comic Sans MS",18))
        self.labelFacts = Label(master, text="Matched Facts", font=("Comic Sans MS",18))
        self.labelRules = Label(master, text="Hit Rules", font=("Comic Sans MS",18))
        self.labelShape = Label(master, text="What shape do you want", font=("Comic Sans MS",12))

        # Konfigurasi button pilih bentuk untuk dibandingkan
        self.b1 = Button(master, text="Segitiga lancip", font=("Comic Sans MS",8), command=lambda:self.compareShape("segitiga-lancip"))
        self.b2 = Button(master, text="Segitiga tumpul", font=("Comic Sans MS",8), command=lambda:self.compareShape("segitiga-tumpul"))
        self.b3 = Button(master, text="Segitiga siku-siku", font=("Comic Sans MS",8), command=lambda:self.compareShape("segitiga-siku"))
        self.b4 = Button(master, text="Segitiga sama kaki dan siku-siku", font=("Comic Sans MS",8), command=lambda:self.compareShape("segitiga-sama-kaki-siku"))
        self.b5 = Button(master, text="Segitiga sama kaki dan tumpul", font=("Comic Sans MS",8), command=lambda:self.compareShape("segitiga-sama-kaki-tumpul"))
        self.b6 = Button(master, text="Segitiga sama kaki dan lancip", font=("Comic Sans MS",8),command=lambda:self.compareShape("segitiga-sama-kaki-lancip"))
        self.b7 = Button(master, text="Segitiga sama sisi", font=("Comic Sans MS",8),command=lambda:self.compareShape("segitiga-sama-sisi"))
        self.b8 = Button(master, text="Segiempat beraturan", font=("Comic Sans MS",8),command=lambda:self.compareShape("persegi"))
        self.b9 = Button(master, text="Segitiga berbentuk layang-layang", font=("Comic Sans MS",8),command=lambda:self.compareShape("layang-layang"))
        self.b10 = Button(master, text="Trapezium sama kaki", font=("Comic Sans MS",8),command=lambda:self.compareShape("trapesium-sama-kaki"))
        self.b11 = Button(master, text="Trapezium rata kanan", font=("Comic Sans MS",8),command=lambda:self.compareShape("trapesium-rata-kanan"))
        self.b12 = Button(master, text="Trapezium rata kiri", font=("Comic Sans MS",8),command=lambda:self.compareShape("trapesium-rata-kiri"))
        self.b13 = Button(master, text="Segi lima sama sisi", font=("Comic Sans MS",8),command=lambda:self.compareShape("segilima-sama-sisi"))
        self.b14 = Button(master, text="Segi enam sama sisi", font=("Comic Sans MS",8),command=lambda:self.compareShape("segienam-sama-sisi"))

        # Konfigurasi hasil detection result, matched facts, hit rules
        self.detectionResult, self.detectionResult_text = "", StringVar()
        self.detectionResult_text.set(self.detectionResult)
        self.detectionResult_label = Label(master, textvariable=self.detectionResult_text, borderwidth=2, width=15, height = 5, relief="groove", font=("Comic Sans MS",25))

        self.matchedFacts, self.matchedFacts_text = "", StringVar()
        self.matchedFacts_text.set(self.matchedFacts)
        self.matchedFacts_label = Label(master, textvariable=self.matchedFacts_text, borderwidth=2, width=28, height = 9, relief="groove", font=("Comic Sans MS",15))

        self.hitRules, self.hitRules_text = "", StringVar()
        self.hitRules_text.set(self.hitRules)
        self.hitRules_label = Label(master, textvariable=self.hitRules_text, borderwidth=2, width=28, height = 9, relief="groove", font=("Comic Sans MS",15))



        # Pemosisian semua elemen ke layar
        self.labelSouImage.place(x=100, y=50)
        self.labelDestImage.place(x=780, y=50)
        self.labelDetection.place(x=100, y=400) 
        self.labelFacts.place(x=450, y=400)  
        self.labelRules.place(x=780, y=400)
        self.labelShape.place(x=1050, y=250)  
        self.source_img.place(x=100, y=90)
        self.det_img.place(x=670, y=90)
        self.img_button.place(x=1050, y=50)
        self.rule_edit_button.place(x=1050, y=90)
        self.rules_button.place(x=1050, y=130)
        self.facts_button.place(x=1050, y=170)
        self.exite_button.place(x=1050, y=210)
        self.b1.place(x=1050, y=280) 
        self.b2.place(x=1050, y=310)
        self.b3.place(x=1050, y=340)
        self.b4.place(x=1050, y=370)
        self.b5.place(x=1050, y=400)
        self.b6.place(x=1050, y=430)
        self.b7.place(x=1050, y=460)
        self.b8.place(x=1050, y=490)
        self.b9.place(x=1050, y=520)
        self.b10.place(x=1050, y=550)
        self.b11.place(x=1050, y=580)
        self.b12.place(x=1050, y=610)
        self.b13.place(x=1050, y=640)
        self.b14.place(x=1050, y=670)
        self.detectionResult_label.place(x=60, y=450)
        self.matchedFacts_label.place(x=400, y=450)
        self.hitRules_label.place(x=710, y=450)
    
		#konfigurasi button untuk hovering mouse
        # self.img_button.bind("<Enter>", self.on_enter_img)
        # self.img_button.bind("<Leave>", self.on_leave_img)

        # self.rule_edit_button.bind("<Enter>", self.on_enter_rule_edit)
        # self.rule_edit_button.bind("<Leave>", self.on_leave_rule_edit)

        # self.rules_button.bind("<Enter>", self.on_enter_rules_button)
        # self.rules_button.bind("<Leave>", self.on_leave_rules_button)
        
        # self.exite_button.bind("<Enter>", self.on_enter_exite)
        # self.exite_button.bind("<Leave>", self.on_leave_exite)

	# Fungsi yang dijalnkan saat button dipencet
    def retrieve_input(self, area, window):
        inputValue=area.get("1.0","end-1c")
        #NAMA FILENYA NEED EDIT
        outputFile = open("geometri.clp","w")
        outputFile.write(inputValue) 
        outputFile.close()
        window.destroy()

    # Pick source image
    def img_button(self):
        # OPEN IMAGE BASE
        self.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.source_file = self.filename
        # return 1
        im = PIL.Image.open(self.filename)
        im = im.resize((300, 300), PIL.Image.ANTIALIAS)
        photo=ImageTk.PhotoImage(im)  
        self.source_img.configure(image = photo)
        self.source_img.image = photo 

        return self.filename

     # Open rule editor
    def rule_edit(self, master):
        print('rules edit')
        window = Toplevel(master)
        window.wm_title("Edit Rules")
        area = Text(window)
        #NAMA FILENYA NEED EDIT
        file = open("geometri.clp","r")
        content = file.read()
        area.insert("end-1c",content)
        area.pack()
        b = Button(window, text="Save", command=lambda: self.retrieve_input(area, window))
        b.pack()

    # Show rules
    def rules(self, master):
        print('rules button u')
        window = Toplevel(master)
        window.wm_title("Rules")
        scrollbar = Scrollbar(window)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox = Listbox(window)
        listbox.pack(side="left",fill="both",expand=True)
        #INSERT NAMA FILE RULES
        file = open("geometri.clp","r").readlines()
        for i in file:
            listbox.insert(END, i)
        listbox.config(width=50,yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        # content = file.read()
        # print(content)

        
        # lRules = ttk.Label(window, text=content)
        #lRules = Label(window, textvariable=content, relief=RAISED )
        # lRules.pack()
        #window.attributes('-topmost', 'true')
        print('rules button u')

    # Show facts
    # DARI initial fact
    def facts(self, master):
        #INSERT NAMA FILE FACTS
        file = open("fakta.txt","r")
        content = file.read()
        window = Toplevel(master)
        window.wm_title("Facts")
        lFacts = ttk.Label(window, text=content)
        #lRules = Label(window, textvariable=content, relief=RAISED )
        lFacts.pack()
        print('facts')

    def compareShape(self,name):
        # Jalanin fungsinya
        detection(self.source_file)
        file1 = open("matched_facts.txt","r")
        content1 = file1.readlines()

        if (name==content1[-1].split()[-1].rstrip(')')):
            self.detectionResult_text.set("YES")
        else:
            self.detectionResult_text.set("NO")

        im = PIL.Image.open("result.jpg")
        im = im.resize((300, 300), PIL.Image.ANTIALIAS)
        photo=ImageTk.PhotoImage(im)  
        self.det_img.configure(image = photo)
        self.det_img.image = photo 
        
        # matched facts dari e.fact
        file = open("matched_facts.txt","r")
        content = file.read()
        self.matchedFacts_text.set(content)
        rule = open("hit_rules.txt","r")
        contents = rule.read()
        self.hitRules_text.set(contents)

    # Popup on exit
    def exite(self):
        MsgBox = messagebox.askokcancel('!!','Are you sure?',icon='warning')
        if MsgBox == False:
            messagebox.showinfo('Returning...','You will now return to the application')
        else:
            exit()
    
    def on_enter_img(self, event):
        self.img_button.configure(highlightbackground='#6E97D8')

    def on_leave_img(self, enter):
        self.img_button.configure(highlightbackground='white')
        
    def on_enter_rule_edit(self, event):
        self.rule_edit_button.configure(highlightbackground='#6E97D8')
        
    def on_leave_rule_edit(self, enter):
        self.rule_edit_button.configure(highlightbackground='white')
        
    def on_enter_rules_button(self, event):
        self.rules_button.configure(highlightbackground='#C93434')

    def on_leave_rules_button(self, enter):
        self.rules_button.configure(highlightbackground='white')
    
    def on_enter_exite(self, event):
        self.exite_button.configure(highlightbackground='#C93434')

    def on_leave_exite(self, enter):
        self.exite_button.configure(highlightbackground='white')
