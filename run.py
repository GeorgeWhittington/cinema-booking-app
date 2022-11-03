from tkinter import Tk, Image

from windows import MainWindow, LoginWindow

if __name__ == "__main__":
    root = Tk()

    icon_img = Image("photo", file="assets/icon.png")
    root.tk.call('wm', 'iconphoto', root._w, icon_img)

    # MainWindow(root).pack(side="top", fill="both", expand=True)
    LoginWindow(root).grid(row=0, column=0)

    root.resizable(False, False)

    root.mainloop()
