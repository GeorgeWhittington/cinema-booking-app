import tkinter as tk

from windows import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
