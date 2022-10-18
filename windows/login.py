from tkinter import *

from PIL import ImageTk, Image

 

class login(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        parent.title("Horizon Cinemas Booking")
        parent.iconbitmap("./icon_2.ico")

        global my_img

        my_img = ImageTk.PhotoImage(Image.open("./icon.jpg"))
        img_label = Label(parent, image=my_img)
        img_label.pack()

        e = Entry(parent, width=50, borderwidth=5)
        e.pack()
        e.insert(0, "Username :")
        e1 = Entry(parent, width=50, borderwidth=5)
        e1.pack()
        e1.insert(0, "Password :")

        def myClick():
            myLabel = Label(parent, text="Invlaid Username " + e.get())
            myLabel.pack()

        myButton = Button(parent, text="Login", command=myClick, fg="blue")
        myButton.pack()