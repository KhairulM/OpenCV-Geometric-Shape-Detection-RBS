import tkinter as tk
from tkinter import *
from tkinter import messagebox
#from AppKit import NSScreen
import os
from tesuto import *

#width = int(NSScreen.mainScreen().frame().size.width)
#height = int(NSScreen.mainScreen().frame().size.height)

width = 1080
#1366768
height = 720
class MainProgram(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title_font = font=('Helvetica',30, "bold", "underline")
        
        # container frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (Start, Main):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # numpuk frame di atas frame lainnya
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Start")

    def show_frame(self, page_name):
		#menampilkan frame di tumpukan paling atas
        frame = self.frames[page_name]
        frame.tkraise()

		
class Start(tk.Frame):
	#konfigurasi halaman start
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="KBS GAME", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.button1 = tk.Button(self, text="CLIK TO PLAY", font =("Hobo Std", 35, "bold"),
                            command=lambda: controller.show_frame("Main"))
        self.button1.pack(pady=250)
        self.button1.bind("<Enter>", self.on_enter_button1)
        self.button1.bind("<Leave>", self.on_leave_button1)

    def on_enter_button1(self, event):
        self.button1.configure(highlightbackground='#e82278')

    def on_leave_button1(self, enter):
        self.button1.configure(highlightbackground='white')
#Konfigurasi  halaman 'Play' yaitu saat click to play
class Main(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		deck = Deck(self) #mengerjakan kelas Deck dari tesuto.py
		



if __name__ == "__main__":
	root = MainProgram()
	root.geometry(str(width)+'x'+str(height))
	root.mainloop()
	if os.path.isfile('cards.png'):
		os.remove('cards.png')


	
