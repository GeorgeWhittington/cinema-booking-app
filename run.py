from tkinter import Tk
from windows import MainWindow
from windows import login

if __name__ == "__main__":
    root = Tk()
    MainWindow(root).pack(side="top", fill="both", expand=True)
    login(root).pack()
    root.mainloop()
