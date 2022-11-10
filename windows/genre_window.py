from tkinter import ttk, StringVar, Listbox
from PIL import ImageTk, Image

from database_models import session, Genre

class GenreWindow(ttk.Frame):
    """Window which allows Admins/Manager to view and edit film genres."""
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        self.all_genres = session.query(Genre).order_by(Genre.name).all()
        self.genre_choices = StringVar(value=[genre.name for genre in self.all_genres])
        self.genre_listbox = Listbox(self, listvariable=self.genre_choices, height=10)

        self.name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self)

        self.add_icon = ImageTk.PhotoImage(Image.open("assets/plus-solid.png").resize((15, 15)))
        self.add_genre_button = ttk.Button(
            self, text="Add", image=self.add_icon,
            compound="left", command=self.add_genre)
        
        self.delete_icon = ImageTk.PhotoImage(Image.open("assets/trash-solid.png").resize((15, 15)))
        self.delete_genre_button = ttk.Button(
            self, text="Delete", image=self.delete_icon,
            compound="left", command=self.delete_genre)
        self.delete_genre_button.state(["disabled"])  # Requires a selection to work, begins disabled
        
        self.update_icon = ImageTk.PhotoImage(Image.open("assets/pen-solid.png").resize((15, 15)))
        self.update_genre_button = ttk.Button(
            self, text="Update", image=self.update_icon,
            compound="left", command=self.update_genre)
        self.update_genre_button.state(["disabled"])  # Requires a selection to work, begins disabled

        self.genre_listbox.grid(column=0, row=0, rowspan=4, sticky="nsew")

        self.name_label.grid(column=1, row=0, padx=2, sticky="w")
        self.name_entry.grid(column=2, row=0, sticky="ew")

        self.add_genre_button.grid(column=1, row=1, columnspan=2, sticky="nsew")
        self.delete_genre_button.grid(column=1, row=2, columnspan=2, sticky="nsew")
        self.update_genre_button.grid(column=1, row=3, columnspan=2, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=6)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)

    def add_genre(self):
        pass

    def update_genre(self):
        pass

    def delete_genre(self):
        pass