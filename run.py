from tkinter import Tk, Image

from windows import MainWindow, LoginWindow
from database_models import session_scope, User, Cinema, City, Authority

if __name__ == "__main__":
    with session_scope() as session:
        admin_user = session.query(User).filter_by(username="manager").first()
        if not admin_user:
            city = City(name="Bristol", morning_price=6.0, afternoon_price=7.0, evening_price=8.0)
            cinema = Cinema(city=city, name="Cabot Circus")
            user = User(
                username="manager",
                password=User.hash_password("pass"),
                cinema=cinema,
                authority=Authority.MANAGER)

            session.add(city)
            session.add(cinema)
            session.add(user)

    root = Tk()

    icon_img = Image("photo", file="assets/icon.png")
    root.tk.call('wm', 'iconphoto', root._w, icon_img)

    # MainWindow(root).pack(side="top", fill="both", expand=True)
    LoginWindow(root).grid(row=0, column=0)
    root.mainloop()
