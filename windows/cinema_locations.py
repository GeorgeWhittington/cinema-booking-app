from tkinter import ttk, StringVar, Listbox, messagebox
from PIL import ImageTk, Image

from database_models import session, Cinema

class LocationWindow(ttk.Frame):
    """Window which allows Admins/Manager to view and edit film genres."""
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        # Widget Creation
        self.all_cinemas = [Cinema.name for cinema in session.query(Cinema).order_by(Cinema.name).all()]
        self.cinema_choices = StringVar(value=self.all_cinemas)
        self.cinema_listbox = Listbox(self, listvariable=self.cinema_choices, height=10)
        self.cinema_listbox.bind("<<ListboxSelect>>", self.cinema_select)

        self.selected_name_label_1 = ttk.Label(self, text="Selected Cinema:")
        self.selected_name_label_2 = ttk.Label(self)

        self.new_name_label = ttk.Label(self, text="New Cinema Name:")
        self.new_name_entry = ttk.Entry(self)

        self.button_frame = ttk.Frame(self)

        self.add_cinema_button = ttk.Button(
            self.button_frame, text="Add", image=parent.add_icon,
            compound="left", command=self.add_cinema)

        self.delete_cinema_button = ttk.Button(
            self.button_frame, text="Delete", image=parent.delete_icon,
            compound="left", command=self.delete_cinema)
        self.delete_cinema_button.state(["disabled"])  # Requires a selection to work, begins disabled

        self.update_cinema_button = ttk.Button(
            self.button_frame, text="Update", image=parent.update_icon,
            compound="left", command=self.update_cinema)
        self.update_cinema_button.state(["disabled"])  # Requires a selection to work, begins disabled

        # Gridding
        self.cinema_listbox.grid(column=0, row=0, rowspan=3, sticky="nsew")

        self.selected_name_label_1.grid(column=1, row=0, padx=(3, 0), sticky="w")
        self.selected_name_label_2.grid(column=2, row=0, sticky="w")

        self.new_name_label.grid(column=1, row=1, padx=(3, 0), sticky="w")
        self.new_name_entry.grid(column=2, row=1, sticky="ew")

        self.button_frame.grid(column=1, row=2, padx=(3, 0), columnspan=2, sticky="n")

        self.add_cinema_button.grid(column=0, row=0)
        self.delete_cinema_button.grid(column=1, padx=(3, 0), row=0)
        self.update_cinema_button.grid(column=2, padx=(3, 0), row=0)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

    def unselect(self):
        """Clear selection."""
        self.selected_name_label_2["text"] = ""
        self.delete_cinema_button.state(["disabled"])
        self.update_cinema_button.state(["disabled"])

    def check_not_empty(self, error_message):
        """Checks if there is a value in the genre selection label.

        If there is, returns this value, if there isn't displays an error popup
        and returns None."""
        selected_cinema = self.selected_name_label_2["text"].strip()
        if not selected_cinema:
            messagebox.showerror(title="Error", message=error_message)
            self.unselect()  # No selection, disable buttons that require one

        return selected_cinema

    def check_cinema_exists(self, cinema_name):
        """Checks if the genre provided exists, displays an error if not."""
        genre = session.query(Cinema).filter_by(name=cinema_name).first()
        if not genre:
            messagebox.showerror(title="Error", message=f"The genre '{cinema_name}' no longer exists")

        return genre

    def cinema_select(self, event):
        """Listens to the listbox select virtual event.

        This data is used to activate the update/delete buttons,
        and keep selected genre label up to date."""
        try:
            selected_id = int(self.cinema_listbox.curselection()[0])
        except IndexError:
            return

        # Selection made, can enable update/delete
        self.delete_cinema_button.state(["!disabled"])
        self.update_cinema_button.state(["!disabled"])

        # Insert name of the currently selected genre into the selected genre label
        self.selected_name_label_2["text"] = self.all_cinemas[selected_id]

    def add_cinema(self):
        cinema_name = self.new_name_entry.get().strip()
        if not cinema_name:
            messagebox.showerror(title="Error", message="Cannot add a cinema with an empty name")
            return

        if session.query(Cinema).filter_by(name=cinema_name).first():
            messagebox.showerror(title="Error", message=f"The cinema '{cinema_name}' cannot be created, it already exists")
            return

        new_cinema = Cinema(name=cinema_name)
        session.add(new_cinema)
        session.commit()

        self.all_genres.append(new_cinema.name)
        self.genre_choices.set(self.all_genres)

    def update_cinema(self):
        if not (selected_cinema := self.check_not_empty("Please select a cinema to update")):
            return

        new_cinema_name = self.new_name_entry.get().strip()
        if not new_cinema_name:
            messagebox.showerror(title="Error", message="Cannot update a cinema to an empty name")
            return

        if selected_cinema == new_cinema_name:
            return

        if not (genre := self.check_genre_exists(selected_cinema)):
            return

        if session.query(Cinema).filter_by(name=new_cinema_name).first():
            messagebox.showerror(title="Error", message=f"The cinema '{new_cinema_name}' already exists")
            return

        Cinema.name = new_cinema_name
        session.commit()

        # Update genre listbox and surrounding state
        for i, c in enumerate(self.all_cinemas):
            if c == selected_cinema:
                self.all_cinema[i] = new_cinema_name
                break
        self.cinema_choices.set(self.all_cinemas)

        self.unselect()

    def delete_cinema(self):
        if not (selected_cinema := self.check_not_empty(error_message="Please select a cinema to delete")):
            return

        if not (cinema := self.check_cinema_exists(selected_cinema)):
            return

        choice = messagebox.askyesno(
            message=f"Are you sure you want to delete the cinema '{selected_cinema}'?",
            title="Delete", icon="question")

        if not choice:
            return

        session.delete(cinema)

        self.all_cinemas.remove(selected_cinema)
        self.cinema_choices.set(self.all_cinemas)

        self.unselect()