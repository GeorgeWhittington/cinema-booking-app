from tkinter import ttk
from PIL import ImageTk, Image


class LoginWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, borderwidth=5)
        parent.title("Horizon Cinemas Booking")

        self.banner_image = ImageTk.PhotoImage(Image.open("assets/banner.jpg"))
        self.img_label = ttk.Label(parent, image=self.banner_image)
        self.img_label.grid(column=0, row=0, columnspan=2, sticky=("E", "W"))

        self.username_label = ttk.Label(parent, text="Username:")
        self.username_entry = ttk.Entry(parent)
        self.username_label.grid(column=0, row=1, sticky=("E",))
        self.username_entry.grid(column=1, row=1, sticky=("E", "W"))

        self.password_label = ttk.Label(parent, text="Password:")
        self.password_entry = ttk.Entry(parent, show="*")
        self.password_label.grid(column=0, row=2, sticky=("E",))
        self.password_entry.grid(column=1, row=2, sticky=("E", "W"))

        self.login_button = ttk.Button(parent, text="Login", command=self.login_click)
        self.login_button.grid(column=0, row=3, columnspan=2)

        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=5)

    def login_click(self):
        print(f"Username: '{self.username_entry.get()}' Password: '{self.password_entry.get()}'")
        pass
        # myLabel = ttk.Label(self.master, text="Invalid Username " + self.username_entry.get())
        # myLabel.pack()
