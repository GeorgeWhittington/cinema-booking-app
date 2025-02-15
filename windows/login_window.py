from tkinter import ttk, messagebox
from PIL import ImageTk, Image

from windows import NewBooking
from database_models import session, User


class LoginWindow(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.banner_image = ImageTk.PhotoImage(Image.open("assets/banner.jpg").resize((666, 161)))
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
        user = session.query(User).filter_by(username=self.username_entry.get()).first()

        if not user:
            messagebox.showerror(title="Please try again", message="Invalid username/password, please try again")
            return

        if user.verify_password(self.password_entry.get()):
            self.master.current_user = user
            self.master.add_menu()
            self.master.switch_window(NewBooking)
            return

        messagebox.showerror(title="Please try again", message="Invalid username/password, please try again")
