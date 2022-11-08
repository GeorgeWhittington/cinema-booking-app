from tkinter import Image

from windows import CinemaApplication, LoginWindow

if __name__ == "__main__":
    root = CinemaApplication()

    # Set icon for application
    root.icon_img = Image("photo", file="assets/icon.png")
    root.tk.call("wm", "iconphoto", root._w, root.icon_img)

    root.title("Horizon Cinemas Booking")

    root.minsize(500, 200)

    # Configure Preferences menu item for MacOS
    root.createcommand("tk::mac::ShowPreferences", CinemaApplication.show_preferences_dialog)

    root.current_window = None
    root.switch_window(LoginWindow, resizeable=False)

    root.mainloop()
