from tkinter import ttk
from PIL import ImageTk, Image

from database_models import session_scope, User


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
        self.username_entry.grid(column=1, row=1, sticky=("W",))

        self.password_label = ttk.Label(parent, text="Password:")
        self.password_entry = ttk.Entry(parent, show="*")
        self.password_label.grid(column=0, row=2, sticky=("E",))
        self.password_entry.grid(column=1, row=2, sticky=("W",))

        self.login_button = ttk.Button(parent, text="Login", command=self.click_login)
        self.login_button.grid(column=0, row=3, columnspan=2)

        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

    def click_login(self):
        with session_scope() as session:
            user = session.query(User).filter_by(username=self.username_entry.get()).first()

            if user.verify_password(self.password_entry.get()):
                print("Password matches")
                return
            
            print("Invalid password, please try again")
