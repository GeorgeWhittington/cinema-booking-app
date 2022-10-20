from tkinter import Tk, Image

from windows import MainWindow, LoginWindow
from database_models import session_scope, User

if __name__ == "__main__":
    with session_scope() as session:
        new_user = User(username="admin", password="pass")
        session.add(new_user)

    root = Tk()

    icon_img = Image("photo", file="assets/icon.png")
    root.tk.call('wm', 'iconphoto', root._w, icon_img)

    # MainWindow(root).pack(side="top", fill="both", expand=True)
    LoginWindow(root).grid(row=0, column=0)
    root.mainloop()
