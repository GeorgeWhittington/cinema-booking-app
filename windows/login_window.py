from tkinter import ttk
from PIL import ImageTk, Image

from windows import MainWindow
from database_models import session_scope, User


class LoginWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.banner_image = ImageTk.PhotoImage(Image.open("assets/banner.jpg"))
        self.img_label = ttk.Label(self, image=self.banner_image)
        self.img_label.grid(column=0, row=0, columnspan=2, sticky="ew")

        self.username_label = ttk.Label(self, text="Username:")
        self.username_entry = ttk.Entry(self)
        self.username_label.grid(column=0, row=1, sticky="e")
        self.username_entry.grid(column=1, row=1, sticky="w")

        self.password_label = ttk.Label(self, text="Password:")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_label.grid(column=0, row=2, sticky="e")
        self.password_entry.grid(column=1, row=2, sticky="w")

        self.login_button = ttk.Button(self, text="Login", command=self.click_login)
        self.login_button.grid(column=0, row=3, columnspan=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def click_login(self):
        with session_scope() as session:
            user = session.query(User).filter_by(username=self.username_entry.get()).first()

            if user.verify_password(self.password_entry.get()):
                self.master.current_user = user
                self.master.add_menu()
                self.master.switch_window(MainWindow)
                return
            
            # TODO: Popup saying this instead
            print("Invalid password, please try again")
