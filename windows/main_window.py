from tkinter import ttk
from PIL import ImageTk, Image


class MainWindow(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.banner_image = ImageTk.PhotoImage(Image.open("assets/banner.jpg"))
        self.img_label = ttk.Label(self, image=self.banner_image)
        self.img_label.grid(column=0, row=0, columnspan=2, sticky="ew")

        self.label = ttk.Label(self, text=f"Hello {parent.current_user.username}")
        self.label.grid(column=0, row=1)

        self.columnconfigure(0, weight=1)