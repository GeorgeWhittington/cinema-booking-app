from tkinter import Tk, Image, ttk

from windows import MainWindow, LoginWindow


# TODO: Consider renaming /windows to /objects and moving this there?
class CinemaApplication(Tk):
    def switch_window(self, window: ttk.Frame, resizeable: bool = True):
        if self.current_window:
            # delete current window
            self.current_window.grid_forget()
            self.current_window.destroy()

        self.current_window = window(self)
        self.current_window.grid(row=0, column=0)

        self.resizable(resizeable, resizeable)

if __name__ == "__main__":
    root = CinemaApplication()

    root.icon_img = Image("photo", file="assets/icon.png")
    root.tk.call("wm", "iconphoto", root._w, root.icon_img)

    root.title("Horizon Cinemas Booking")

    root.current_window = None
    root.switch_window(LoginWindow, resizeable=False)

    root.mainloop()
