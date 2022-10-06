from tkinter import Frame, Label


class MainWindow(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.label = Label(parent, text="Hello World")
        self.label.pack()