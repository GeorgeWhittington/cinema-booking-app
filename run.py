from tkinter import Tk

from windows import MainWindow

if __name__ == "__main__":
    root = Tk()
    MainWindow(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
