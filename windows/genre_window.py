from tkinter import ttk, StringVar, Listbox, messagebox
from PIL import ImageTk, Image

from database_models import session, Genre

class GenreWindow(ttk.Frame):
    """Window which allows Admins/Manager to view and edit film genres."""
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        # Widget Creation
        self.all_genres = [genre.name for genre in session.query(Genre).order_by(Genre.name).all()]
        self.genre_choices = StringVar(value=self.all_genres)
        self.genre_listbox = Listbox(self, listvariable=self.genre_choices, height=10)
        self.genre_listbox.bind("<<ListboxSelect>>", self.genre_select)

        self.selected_name_label_1 = ttk.Label(self, text="Selected Genre:")
        self.selected_name_label_2 = ttk.Label(self)

        self.new_name_label = ttk.Label(self, text="New Genre Name:")
        self.new_name_entry = ttk.Entry(self)

        self.add_genre_button = ttk.Button(
            self, text="Add", image=parent.add_icon,
            compound="left", command=self.add_genre)

        self.delete_genre_button = ttk.Button(
            self, text="Delete", image=parent.delete_icon,
            compound="left", command=self.delete_genre)
        self.delete_genre_button.state(["disabled"])  # Requires a selection to work, begins disabled

        self.update_genre_button = ttk.Button(
            self, text="Update", image=parent.update_icon,
            compound="left", command=self.update_genre)
        self.update_genre_button.state(["disabled"])  # Requires a selection to work, begins disabled

        # Gridding
        self.genre_listbox.grid(column=0, row=0, rowspan=5, sticky="nsew")

        self.selected_name_label_1.grid(column=1, row=0, padx=(3, 0), sticky="w")
        self.selected_name_label_2.grid(column=2, row=0, sticky="w")

        self.new_name_label.grid(column=1, row=1, padx=(3, 0), sticky="w")
        self.new_name_entry.grid(column=2, row=1, sticky="ew")

        self.add_genre_button.grid(column=1, row=2, padx=(3, 0), columnspan=2, sticky="nsew")
        self.delete_genre_button.grid(column=1, row=3, padx=(3, 0), columnspan=2, sticky="nsew")
        self.update_genre_button.grid(column=1, row=4, padx=(3, 0), columnspan=2, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=6)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(4, weight=2)

    def unselect(self):
        """Clear selection."""
        self.selected_name_label_2["text"] = ""
        self.delete_genre_button.state(["disabled"])
        self.update_genre_button.state(["disabled"])

    def check_not_empty(self, error_message):
        """Checks if there is a value in the genre selection label.

        If there is, returns this value, if there isn't displays an error popup
        and returns None."""
        selected_genre = self.selected_name_label_2["text"].strip()
        if not selected_genre:
            messagebox.showerror(title="Error", message=error_message)
            self.unselect()  # No selection, disable buttons that require one

        return selected_genre

    def check_genre_exists(self, genre_name):
        """Checks if the genre provided exists, displays an error if not."""
        genre = session.query(Genre).filter_by(name=genre_name).first()
        if not genre:
            messagebox.showerror(title="Error", message=f"The genre '{genre_name}' no longer exists")
            # TODO: clear nonexistent value from listbox/listbox state (but really it shouldn't be possible for this to happen)

        return genre

    def genre_select(self, event):
        """Listens to the listbox select virtual event.

        This data is used to activate the update/delete buttons,
        and keep selected genre label up to date."""
        try:
            selected_id = int(self.genre_listbox.curselection()[0])
        except IndexError:
            return

        # Selection made, can enable update/delete
        self.delete_genre_button.state(["!disabled"])
        self.update_genre_button.state(["!disabled"])

        # Insert name of the currently selected genre into the selected genre label
        self.selected_name_label_2["text"] = self.all_genres[selected_id]

    def add_genre(self):
        genre_name = self.new_name_entry.get().strip()
        if not genre_name:
            messagebox.showerror(title="Error", message="Cannot add a genre with an empty name")
            return

        if session.query(Genre).filter_by(name=genre_name).first():
            messagebox.showerror(title="Error", message=f"The genre '{genre_name}' cannot be created, it already exists")
            return

        new_genre = Genre(name=genre_name)
        session.add(new_genre)
        session.commit()

        self.all_genres.append(new_genre.name)
        self.genre_choices.set(self.all_genres)

    def update_genre(self):
        if not (selected_genre := self.check_not_empty("Please select a genre to update")):
            return

        new_genre_name = self.new_name_entry.get().strip()
        if not new_genre_name:
            messagebox.showerror(title="Error", message="Cannot update a genre to an empty name")
            return

        if selected_genre == new_genre_name:
            return

        if not (genre := self.check_genre_exists(selected_genre)):
            return

        if session.query(Genre).filter_by(name=new_genre_name).first():
            messagebox.showerror(title="Error", message=f"The genre '{new_genre_name}' already exists")
            return

        genre.name = new_genre_name
        session.commit()

        # Update genre listbox and surrounding state
        for i, g in enumerate(self.all_genres):
            if g == selected_genre:
                self.all_genres[i] = new_genre_name
                break
        self.genre_choices.set(self.all_genres)

        self.unselect()

    def delete_genre(self):
        if not (selected_genre := self.check_not_empty(error_message="Please select a genre to delete")):
            return

        if not (genre := self.check_genre_exists(selected_genre)):
            return

        choice = messagebox.askyesno(
            message=f"Are you sure you want to delete the genre '{selected_genre}'?",
            title="Delete", icon="question")

        if not choice:
            return

        session.delete(genre)

        self.all_genres.remove(selected_genre)
        self.genre_choices.set(self.all_genres)

        self.unselect()