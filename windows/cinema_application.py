from functools import partial
from tkinter import Tk, ttk, Menu, Toplevel

from database_models import session, Authority
from windows import FilmWindow


class CinemaApplication(Tk):
    def switch_window(self, window: ttk.Frame, resizeable: bool = True):
        """Replaces window content.

        Clears the current contents of the window (if there are any)
        and then creates and inserts the new frame that is specified."""
        if self.current_window:
            # delete current window
            self.unbind("<Configure>")  # If a resize callback was bound, unbind it
            self.current_window.grid_forget()
            self.current_window.destroy()

        self.current_window = window(self)
        self.current_window.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # If the window has a resize callback, bind it to the root window
        try:
            self.bind("<Configure>", self.current_window.resize)
        except AttributeError:
            pass

        self.resizable(resizeable, resizeable)

    def add_menu(self):
        """Creates the application Menu.

        It adds only the menu items that the logged in user has permissions for.

        Should only be called after login is sucessful and the
        current_user attribute has been set."""
        self.option_add("*tearOff", False)  # Disable tear-off menus

        self.menubar = Menu(self)
        self["menu"] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menu_edit = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label="File")
        self.menubar.add_cascade(menu=self.menu_edit, label="Edit")
        # TODO: add "About" option which credits any assets used (Images and fontawesome icons) and the coders (Us two!)

        # As and when the windows are built replace with code similar to:
        # self.menu_file.add_command(label="New Booking", command=partial(self.switch_window, self, MainWindow))
        self.menu_file.add_command(label="New Booking", command=partial(print, "New Booking"))
        self.menu_edit.add_command(label="Cancel Booking", command=partial(print, "Cancel Booking"))

        # If not on macos, add a settings option to the edit menu
        if self.tk.call("tk", "windowingsystem") != "aqua":
            self.menu_edit.add_command(label="Settings", command=self.show_preferences_dialog)

        if self.current_user.authority == Authority.BOOKING:
            return

        # Authority not booking, so must have atleast admin permissions
        self.menu_file.add_separator()
        self.menu_file.add_command(label="New Film", command=partial(print, "New Film"))
        self.menu_file.add_command(label="New Film Showing", command=partial(print, "New Film Showing"))
        self.menu_file.add_command(label="New Report", command=partial(print, "New Report"))

        self.menu_edit.add_separator()
        self.menu_edit.add_command(label="Update/Delete Films", command=partial(self.switch_window, FilmWindow))
        self.menu_edit.add_command(label="Update/Delete Film Showings", command=partial(print, "Update/Delete Film Showings"))

        if self.current_user.authority == Authority.ADMIN:
            return

        # Not Admin, so must be manager
        self.menu_file.add_separator()
        self.menu_file.add_command(label="New Location", command=partial(print, "New Location"))

        self.menu_edit.add_separator()
        self.menu_edit.add_command(label="Update/Delete Locations", command=partial(print, "Update/Delete Locations"))

    def show_modal(self, window: ttk.Frame, window_kwargs: dict):
        """Creates a popup window containing the frame specified.

        The root window will be disabled while this popup is open.

        If the window object that gets instantiated sets the attribute
        'result' before exiting using the dismiss function it is passed
        that value will be returned.

        Adapted from the "Rolling Your Own" section at the bottom of
        this page: https://tkdocs.com/tutorial/windows.html
        """
        # TODO: Consider making a Modal class that all modals need to subclass
        # from and exporting some of this logic there (especially dismiss)
        dialog = Toplevel(self)

        def dismiss():
            dialog.grab_release()
            dialog.destroy()

        dialog_frame = window(dialog, dismiss=dismiss, **window_kwargs)
        dialog_frame.grid(column=0, row=0, sticky="nsew")
        dialog.resizable(False, False)

        dialog.protocol("WM_DELETE_WINDOW", dismiss)
        dialog.transient(self)
        dialog.wait_visibility()
        dialog.grab_set()
        dialog.wait_window()

        # Return result, if there is one
        try:
            return dialog_frame.result
        except AttributeError:
            return

    @staticmethod
    def show_preferences_dialog():
        """TODO: Implement a settings popup"""
        print("Preferences accessed")