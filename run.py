from functools import partial
from tkinter import Tk, Image, ttk, Menu

from database_models import session_scope, Authority
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

    def add_menu(self):
        """Menu which adds the menu items that the logged in user has permissions for.

        Should only be called after login is sucessful and the
        current_user attribute has been set."""

        self.option_add("*tearOff", False)  # Disable tear-off menus

        self.menubar = Menu(self)
        self["menu"] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menu_edit = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label="File")
        self.menubar.add_cascade(menu=self.menu_edit, label="Edit")

        # As and when the windows are built replace with code similar to:
        # self.menu_file.add_command(label="New Booking", command=partial(self.switch_window, self, MainWindow))
        self.menu_file.add_command(label="New Booking", command=partial(print, "New Booking"))
        self.menu_edit.add_command(label="Cancel Booking", command=partial(print, "Cancel Booking"))

        # If not on macos, add a settings option to the edit menu
        if self.tk.call("tk", "windowingsystem") != "aqua":
            self.menu_edit.add_command(label="Settings", command=self.show_preferences_dialog)

        with session_scope():
            if self.current_user.authority == Authority.BOOKING:
                return

            # Authority not booking, so must have atleast admin permissions
            self.menu_file.add_separator()
            self.menu_file.add_command(label="New Film", command=partial(print, "New Film"))
            self.menu_file.add_command(label="New Film Showing", command=partial(print, "New Film Showing"))
            self.menu_file.add_command(label="New Report", command=partial(print, "New Report"))

            self.menu_edit.add_separator()
            self.menu_edit.add_command(label="Update/Delete Films", command=partial(print, "Update/Delete Films"))
            self.menu_edit.add_command(label="Update/Delete Films", command=partial(print, "Update/Delete Film Showings"))

            if self.current_user.authority == Authority.ADMIN:
                return

            self.menu_file.add_separator()
            self.menu_file.add_command(label="New Location", command=partial(print, "New Location"))

            self.menu_edit.add_separator()
            self.menu_edit.add_command(label="Update/Delete Locations", command=partial(print, "Update/Delete Locations"))

    @staticmethod
    def show_preferences_dialog():
        """TODO: Implement a settings popup"""


if __name__ == "__main__":
    root = CinemaApplication()

    root.icon_img = Image("photo", file="assets/icon.png")
    root.tk.call("wm", "iconphoto", root._w, root.icon_img)

    root.title("Horizon Cinemas Booking")
    root.createcommand("tk::mac::ShowPreferences", CinemaApplication.show_preferences_dialog)

    root.current_window = None
    root.switch_window(LoginWindow, resizeable=False)

    root.mainloop()
