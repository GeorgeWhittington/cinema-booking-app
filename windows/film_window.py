from datetime import datetime
from io import BytesIO

from cairosvg import svg2png
from tkinter import ttk, messagebox, Text
from PIL import ImageTk, Image

from database_models import session_scope, Film, AgeRatings


class FilmEditWindow(ttk.Frame):
    """Dialog for adding or updating Films.
    
    If 'edit_type' is EDIT then the kwarg 'film' needs to be set to the
    film being edited.
    """

    ADD = "Add"
    EDIT = "Edit"

    def __init__(self, parent, *args, **kwargs):
        self.dismiss = kwargs.pop("dismiss")
        self.edit_type = kwargs.pop("edit_type")
        
        if self.edit_type == FilmEditWindow.ADD:
            parent.title("Add Film")
        
        if self.edit_type == FilmEditWindow.EDIT:
            self.film = kwargs.pop("film")
            with session_scope() as session:
                parent.title(f"Edit Film - {self.film.title}")
        
        super().__init__(parent, *args, **kwargs)

        # Widget Creation
        self.title_label = ttk.Label(self, text="Title:")
        self.year_label = ttk.Label(self, text="Year Published:")
        self.rating_label = ttk.Label(self, text="Rating:")
        self.age_rating_label = ttk.Label(self, text="Age Rating:")
        self.duration_label = ttk.Label(self, text="Duration:")
        self.synopsis_label = ttk.Label(self, text="Synopsis:")
        self.cast_label = ttk.Label(self, text="Cast:")

        self.title_entry = ttk.Entry(self)

        self.year_entry = ttk.Combobox(self)
        self.year_entry["values"] = list(range(1890, datetime.now().year + 1)) # Max year is current year, may want to change this after consulting with Zaheer
        
        self.rating_entry = ttk.Combobox(self)
        self.rating_entry["values"] = list(range(0, 101))
        
        self.age_rating_entry = ttk.Combobox(self)
        self.age_rating_entry["values"] = [age_rating.value for age_rating in AgeRatings]

        self.duration_frame = ttk.Frame(self)

        self.duration_hours = ttk.Combobox(self.duration_frame)
        self.duration_hours["values"] = list(range(0, 100))
        self.hours_label = ttk.Label(self.duration_frame, text="hours")

        self.duration_minutes = ttk.Combobox(self.duration_frame)
        self.duration_minutes["values"] = list(range(0, 60))
        self.minutes_label = ttk.Label(self.duration_frame, text="minutes")

        self.synopsis_entry = Text(self, height=5)  # 5 lines of text high

        self.cast_entry = ttk.Entry(self)

        # Gridding
        widgets = [
            (self.title_label, self.title_entry),
            (self.year_label, self.year_entry),
            (self.rating_label, self.rating_entry),
            (self.age_rating_label, self.age_rating_entry),
            (self.duration_label, self.duration_frame),
            (self.synopsis_label, self.synopsis_entry),
            (self.cast_label, self.cast_entry)
        ]

        for y, (label, entry) in enumerate(widgets):
            label.grid(column=0, row=y, sticky="w")
            entry.grid(column=1, row=y, sticky="ew")

        self.duration_hours.grid(column=0, row=0)
        self.hours_label.grid(column=1, row=0)
        self.duration_minutes.grid(column=2, row=0)
        self.minutes_label.grid(column=3, row=0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Prefilling with existing values if an EDIT window
        if self.edit_type == FilmEditWindow.ADD:
            return
        
        with session_scope() as session:
            self.title_entry.insert(0, self.film.title)
            self.year_entry.set(self.film.year_published)
            self.rating_entry.set(int(self.film.rating * 100))
            self.age_rating_entry.set(self.film.age_rating.value)
            m, s = divmod(self.film.duration.total_seconds(), 60)
            h, m = divmod(m, 60)
            self.duration_hours.set(int(h))
            self.duration_minutes.set(int(m))
            self.synopsis_entry.insert("1.0", self.film.synopsis)  # Inserts at line 1 char 0
            self.cast_entry.insert(0, self.film.cast)


class FilmWindow(ttk.Frame):
    """Window which allows for Admins and Managers to: inspect, add, update and delete films."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.inspected_film_id = None

        self.window_width = None
        self.window_height = None

        # --- Treeview ---
        headings = [
            "Title",
            "Year Published",
            "Age Rating",
            "Duration",
            "Rating"
        ]
        self.treeview = ttk.Treeview(self,
            columns=(i for i in range(len(headings))),
            show="headings",
            selectmode="browse")  # Only allow one row to be selected at once
        self.treeview_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview['yscrollcommand'] = self.treeview_scrollbar.set
        for i, value in enumerate(headings):
            self.treeview.heading(i, text=value)
        for cid in range(len(headings)):
            self.treeview.column(cid, stretch=True)
        self.treeview.bind("<<TreeviewSelect>>", self.treeview_select)

        with session_scope() as session:
            for film in session.query(Film).order_by(Film.title).all():
                m, s = divmod(film.duration.total_seconds(), 60)
                h, m = divmod(m, 60)

                self.treeview.insert(
                    "", "end", iid=film.id,
                    values=(
                        film.title,
                        film.year_published,
                        film.age_rating.value,
                        f"{int(h)}h {int(m)}m",
                        f"{int(film.rating * 100)}/100"
                    ))

        # --- Inspect Film Section ---
        self.inspect_frame = ttk.Frame(self)

        self.inspect_title = ttk.Label(self.inspect_frame, text="Title:")
        self.inspect_year = ttk.Label(self.inspect_frame, text="Year Published:")
        self.inspect_rating = ttk.Label(self.inspect_frame, text="Rating:")
        self.inspect_age_rating = ttk.Label(self.inspect_frame, text="Age Rating:")
        self.inspect_duration = ttk.Label(self.inspect_frame, text="Duration:")
        self.inspect_synopsis = ttk.Label(self.inspect_frame, text="Synopsis:", wraplength=240)
        self.inspect_cast = ttk.Label(self.inspect_frame, text="Cast:", wraplength=240)

        # --- Buttons ---
        self.button_frame = ttk.Frame(self)

        self.add_icon = self.create_icon("assets/plus-solid.svg")
        self.add_film_button = ttk.Button(
            self.button_frame, text="Add", image=self.add_icon,
            compound="left", command=self.add_film)

        self.delete_icon = self.create_icon("assets/trash-solid.svg")
        self.delete_film_button = ttk.Button(
            self.button_frame, text="Delete", image=self.delete_icon,
            compound="left", command=self.delete_film)
        self.delete_film_button.state(["disabled"])  # Requires a selection to work, begins disabled

        self.update_icon = self.create_icon("assets/pen-solid.svg")
        self.update_film_button = ttk.Button(
            self.button_frame, text="Update", image=self.update_icon,
            compound="left", command=self.update_film)
        self.update_film_button.state(["disabled"])  # Requires a selection to work, begins disabled

        self.view_icon = self.create_icon("assets/eye-solid.svg")
        self.view_showings_button = ttk.Button(
            self.button_frame, text="View Showings", image=self.view_icon,
            compound="left", command=self.view_film_showings)

        # --- Gridding ---
        self.treeview.grid(column=0, row=0, sticky="nsew")
        self.treeview_scrollbar.grid(column=1, row=0, sticky="ns")

        self.inspect_frame.grid(column=0, row=1, sticky="nsew")

        for y, widget in enumerate([self.inspect_title, self.inspect_year, self.inspect_rating, self.inspect_age_rating, self.inspect_duration, self.inspect_synopsis, self.inspect_cast]):
            widget.grid(column=0, row=y, sticky="w")
        
        self.button_frame.grid(column=0, row=2, sticky="nsew")

        for x, widget in enumerate([self.add_film_button, self.delete_film_button, self.update_film_button, self.view_showings_button]):
            widget.grid(column=x, row=0)

        self.columnconfigure(0, weight=1)

    @staticmethod
    def create_icon(url):
        out = BytesIO()
        svg2png(url=url, write_to=out)
        return ImageTk.PhotoImage(Image.open(out).resize((15, 15)))

    @staticmethod
    def replace_label(label, new_value):
        current_text = label["text"]
        # We only care about splitting to get the data before the first ':'
        key, _ = current_text.split(":", maxsplit=1)
        label.config(text=f"{key}: {new_value}")

    def treeview_select(self, event):
        """Listens to the treeview select virtual event to update the inspect section."""
        try:
            selected_id = int(self.treeview.selection()[0])
        except IndexError:
            return

        # A selection has been made, so these buttons can be enabled
        self.delete_film_button.state(["!disabled"])
        self.update_film_button.state(["!disabled"])

        if self.inspected_film_id == int(self.treeview.selection()[0]):
            return

        with session_scope() as session:
            selected_film = session.query(Film).get(selected_id)
            if not selected_film:  # This shouldn't happen, but we can't continue if it somehow does
                return

            self.inspected_film_id = selected_film.id
            
            m, s = divmod(selected_film.duration.total_seconds(), 60)
            h, m = divmod(m, 60)

            self.replace_label(self.inspect_title, selected_film.title)
            self.replace_label(self.inspect_year, selected_film.year_published)
            self.replace_label(self.inspect_rating, f"{int(selected_film.rating * 100)}/100")
            self.replace_label(self.inspect_age_rating, selected_film.age_rating.value)
            self.replace_label(self.inspect_duration, f"{int(h)}h {int(m)}m")
            self.replace_label(self.inspect_synopsis, selected_film.synopsis)
            self.replace_label(self.inspect_cast, selected_film.cast)
    
    def resize(self, event):
        """Listens to configure events on this window.
        
        Detects if window size has changed and uses this data to adjust
        where labels should wrap."""
        if type(event.widget) != type(self.master):
            return

        if (self.window_width == event.width) and (self.window_height == event.height):
            return

        self.inspect_synopsis.configure(wraplength=event.width - 10)
        self.inspect_cast.configure(wraplength=event.width - 10)

        self.window_width = event.width
        self.window_height = event.height

    def add_film(self):
        self.master.show_modal(FilmEditWindow, {"edit_type": FilmEditWindow.ADD})

    def delete_film(self):
        selected_id = int(self.treeview.selection()[0])

        with session_scope() as session:
            selected_film = session.query(Film).get(selected_id)
            if not selected_film:  # This shouldn't happen, but we can't continue if it somehow does
                return

            confirm = messagebox.askyesno(
                message=f"Are you sure you want to delete the film {selected_film.title}?",
                title="Delete", icon="question")

            if not confirm:
                return

            session.delete(selected_film)
            self.treeview.delete(str(selected_id))
        
        # film deleted -> selection cleared, so delete and update buttons need to be disabled again
        self.delete_film_button.state(["disabled"])
        self.update_film_button.state(["disabled"])

    def update_film(self):
        selected_id = int(self.treeview.selection()[0])

        with session_scope() as session:
            film = session.query(Film).get(selected_id)
            if not film:
                return

        self.master.show_modal(FilmEditWindow, {
            "edit_type": FilmEditWindow.EDIT,
            "film": film
        })

    def view_film_showings(self):
        pass