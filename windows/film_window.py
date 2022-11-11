from datetime import datetime, timedelta

from tkinter import ttk, messagebox, Text, Listbox, StringVar
from PIL import ImageTk, Image

from database_models import session, Film, Genre, AgeRatings
from misc.constants import OLDEST_FILM_YEAR, LONGEST_FILM_HOURS
from misc.utils import get_hours_minutes


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
            parent.title(f"Edit Film - {self.film.title}")

        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        # Widget Creation
        self.title_label = ttk.Label(self, text="Title:")
        self.year_label = ttk.Label(self, text="Year Published:")
        self.rating_label = ttk.Label(self, text="Rating:")
        self.age_rating_label = ttk.Label(self, text="Age Rating:")
        self.duration_label = ttk.Label(self, text="Duration:")
        self.synopsis_label = ttk.Label(self, text="Synopsis:")
        self.cast_label = ttk.Label(self, text="Cast:")
        self.genres_label = ttk.Label(self, text="Genres:")

        self.title_entry = ttk.Entry(self)

        self.year_entry = ttk.Spinbox(self, from_=OLDEST_FILM_YEAR, to=datetime.now().year)  # Max year is current year, may want to change this after consulting with Zaheer

        self.rating_entry = ttk.Spinbox(self, from_=0, to=100)

        self.age_rating_entry = ttk.Combobox(self)
        self.age_rating_entry["values"] = [age_rating.value for age_rating in AgeRatings]

        self.duration_frame = ttk.Frame(self)

        self.duration_hours = ttk.Spinbox(self.duration_frame, from_=0, to=LONGEST_FILM_HOURS)
        self.hours_label = ttk.Label(self.duration_frame, text="hours")

        self.duration_minutes = ttk.Spinbox(self.duration_frame, from_=0, to=59)
        self.minutes_label = ttk.Label(self.duration_frame, text="minutes")

        self.synopsis_entry = Text(self, height=5)  # 5 lines of text high

        self.cast_entry = ttk.Entry(self)

        self.all_genres = session.query(Genre).order_by(Genre.name).all()
        self.genre_choices = StringVar(value=[genre.name for genre in self.all_genres])
        self.genres_entry = Listbox(self, listvariable=self.genre_choices, height=5, selectmode="extended")

        self.button_frame = ttk.Frame(self)
        self.submit_button = ttk.Button(self.button_frame, text=self.edit_type, command=self.submit)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.dismiss)

        # Gridding
        widgets = [
            (self.title_label, self.title_entry),
            (self.year_label, self.year_entry),
            (self.rating_label, self.rating_entry),
            (self.age_rating_label, self.age_rating_entry),
            (self.duration_label, self.duration_frame),
            (self.synopsis_label, self.synopsis_entry),
            (self.cast_label, self.cast_entry),
            (self.genres_label, self.genres_entry)
        ]

        for y, (label, entry) in enumerate(widgets):
            label.grid(column=0, row=y, pady=2, sticky="w")
            entry.grid(column=1, row=y, pady=2, sticky="ew")

        self.button_frame.grid(column=1, row=len(widgets))
        self.submit_button.grid(column=0, row=0)
        self.cancel_button.grid(column=1, row=0)

        self.duration_hours.grid(column=0, row=0)
        self.hours_label.grid(column=1, row=0)
        self.duration_minutes.grid(column=2, row=0)
        self.minutes_label.grid(column=3, row=0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Prefilling with existing values if an EDIT window
        if self.edit_type == FilmEditWindow.ADD:
            return

        self.title_entry.insert(0, self.film.title)
        self.year_entry.set(self.film.year_published)
        self.rating_entry.set(int(self.film.rating * 100))
        self.age_rating_entry.set(self.film.age_rating.value)
        h, m = get_hours_minutes(self.film.duration.total_seconds())
        self.duration_hours.set(int(h))
        self.duration_minutes.set(int(m))
        self.synopsis_entry.insert("1.0", self.film.synopsis)  # Inserts at line 1 char 0
        self.cast_entry.insert(0, self.film.cast)

        selected_genres = [genre.name for genre in self.film.genres]
        listbox_genre_ids = [i for i, genre in enumerate(self.all_genres) if genre.name in selected_genres]
        for genre_id in listbox_genre_ids:
            self.genres_entry.select_set(genre_id)

    def submit(self):
        """Verifies all data provided and then either creates or updates a film object."""
        # Verify all data provided is valid before proceeding
        def test_empty(value, name):
            if not value.strip():
                raise ValueError(f"{name} cannot be empty")
            try:
                return int(value)
            except ValueError:
                raise ValueError(f"{name} needs to be a number")

        try:
            if not self.title_entry.get().strip():
                raise ValueError("Film title cannot be empty")

            year = test_empty(self.year_entry.get(), "Publishing year")
            if year < OLDEST_FILM_YEAR or year > datetime.now().year:
                raise ValueError(f"The publishing year {year} is invalid")

            rating = test_empty(self.rating_entry.get(), "Film rating")
            if rating < 0 or rating > 100:
                raise ValueError(f"The rating {rating} is not between 0 and 100")

            if not self.age_rating_entry.get().strip():
                raise ValueError("Age rating cannot be empty")

            if self.age_rating_entry.get() not in [age_rating.value for age_rating in AgeRatings]:
                raise ValueError(f"The age rating {self.age_rating_entry.get()} is not valid")

            hours = test_empty(self.duration_hours.get(), "Film duration hours")
            minutes = test_empty(self.duration_minutes.get(), "Film duration minutes")

            if hours < 0 or hours > LONGEST_FILM_HOURS or minutes < 0 or minutes > 59:
                raise ValueError(f"The duration {hours}h{minutes}m is invalid")

            if not self.synopsis_entry.get('1.0', 'end').strip():
                raise ValueError("Film synopsis cannot be empty")

            if not self.cast_entry.get().strip():
                raise ValueError("Film cast cannot be empty")
        except ValueError as e:
            messagebox.showerror(title="Invalid film data", message=e)
            return

        for r in AgeRatings:
            if r.value == self.age_rating_entry.get():
                age_rating = r

        genres = []
        for sel_id in self.genres_entry.curselection():
            genres.append(self.all_genres[sel_id])

        if self.edit_type == FilmEditWindow.ADD:
            self.result = self.add_film(age_rating, genres)
        elif self.edit_type == FilmEditWindow.EDIT:
            self.edit_film(age_rating, genres)

        self.dismiss()

    def add_film(self, age_rating, genres):
        new_film = Film(
            title=self.title_entry.get().strip(),
            year_published=int(self.year_entry.get()),
            rating=int(self.rating_entry.get()) / 100.0,
            age_rating=age_rating,
            duration=timedelta(hours=int(self.duration_hours.get()), minutes=int(self.duration_minutes.get())),
            synopsis=self.synopsis_entry.get('1.0', 'end').strip(),
            cast=self.cast_entry.get().strip(),
            genres=genres)
        session.add(new_film)
        session.commit()

        return new_film

    def edit_film(self, age_rating, genres):
        self.film.title = self.title_entry.get().strip()
        self.film.year_published = int(self.year_entry.get())
        self.film.rating = int(self.rating_entry.get()) / 100.0
        self.film.age_rating = age_rating
        self.film.duration = timedelta(hours=int(self.duration_hours.get()), minutes=int(self.duration_minutes.get()))
        self.film.synopsis = self.synopsis_entry.get('1.0', 'end').strip()
        self.film.cast = self.cast_entry.get().strip()
        self.film.genres = genres

        session.commit()


class FilmWindow(ttk.Frame):
    """Window which allows for Admins and Managers to: inspect, add, update and delete films."""
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
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

        for film in session.query(Film).order_by(Film.title).all():
            self.treeview_insert(film)

        # --- Inspect Film Section ---
        self.inspect_frame = ttk.Frame(self)

        self.inspect_title = ttk.Label(self.inspect_frame, text="Title:", wraplength=240)
        self.inspect_year = ttk.Label(self.inspect_frame, text="Year Published:")
        self.inspect_rating = ttk.Label(self.inspect_frame, text="Rating:")
        self.inspect_age_rating = ttk.Label(self.inspect_frame, text="Age Rating:")
        self.inspect_duration = ttk.Label(self.inspect_frame, text="Duration:")
        self.inspect_synopsis = ttk.Label(self.inspect_frame, text="Synopsis:", wraplength=240)
        self.inspect_cast = ttk.Label(self.inspect_frame, text="Cast:", wraplength=240)
        self.inspect_genres = ttk.Label(self.inspect_frame, text="Genres:", wraplength=240)

        # --- Buttons ---
        self.button_frame = ttk.Frame(self)

        self.add_film_button = ttk.Button(
            self.button_frame, text="Add", image=parent.add_icon,
            compound="left", command=self.add_film)

        self.delete_film_button = ttk.Button(
            self.button_frame, text="Delete", image=parent.delete_icon,
            compound="left", command=self.delete_film)
        self.delete_film_button.state(["disabled"])  # Requires a selection to work, begins disabled

        self.update_film_button = ttk.Button(
            self.button_frame, text="Update", image=parent.update_icon,
            compound="left", command=self.update_film)
        self.update_film_button.state(["disabled"])  # Requires a selection to work, begins disabled

        self.view_showings_button = ttk.Button(
            self.button_frame, text="View Showings", image=parent.view_icon,
            compound="left", command=self.view_film_showings)

        # --- Gridding ---
        self.treeview.grid(column=0, row=0, sticky="nsew")
        self.treeview_scrollbar.grid(column=1, row=0, sticky="ns")

        self.inspect_frame.grid(column=0, row=1, sticky="nsew")

        for y, widget in enumerate([self.inspect_title, self.inspect_year, self.inspect_rating, self.inspect_age_rating, self.inspect_duration, self.inspect_synopsis, self.inspect_cast, self.inspect_genres]):
            widget.grid(column=0, row=y, sticky="w")

        self.button_frame.grid(column=0, row=2, sticky="nsew")

        for x, widget in enumerate([self.add_film_button, self.delete_film_button, self.update_film_button, self.view_showings_button]):
            widget.grid(column=x, row=0)

        self.columnconfigure(0, weight=1)

    @staticmethod
    def replace_label(label, new_value):
        """Edits a label widget so that new_value is displayed after it's first ':'"""
        current_text = label["text"]
        # We only care about splitting to get the data before the first ':'
        key, _ = current_text.split(":", maxsplit=1)
        label["text"] = f"{key}: {new_value}"

    def treeview_insert(self, film):
        h, m = get_hours_minutes(film.duration.total_seconds())

        self.treeview.insert(
            "", "end", iid=film.id,
            values=(
                film.title,
                film.year_published,
                film.age_rating.value,
                film.string_conv("duration"),
                film.string_conv("rating")))

    def treeview_sort(self):
        """Sort treeview by Title column."""
        # Fetch the contents of the title column and the iid for each item in the tree
        children = [(self.treeview.set(iid, 0), iid) for iid in self.treeview.get_children()]
        children.sort(key=lambda child: child[0])  # Sort by title

        # Rearrange items in sorted position
        for index, (_, iid) in enumerate(children):
            self.treeview.move(iid, "", index)

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

        selected_film = session.query(Film).get(selected_id)
        if not selected_film:  # This shouldn't happen, but we can't continue if it somehow does
            return

        self.inspected_film_id = selected_film.id

        h, m = get_hours_minutes(selected_film.duration.total_seconds())

        self.replace_label(self.inspect_title, selected_film.title)
        self.replace_label(self.inspect_year, selected_film.year_published)
        self.replace_label(self.inspect_rating, selected_film.string_conv("rating"))
        self.replace_label(self.inspect_age_rating, selected_film.age_rating.value)
        self.replace_label(self.inspect_duration, selected_film.string_conv("duration"))
        self.replace_label(self.inspect_synopsis, selected_film.synopsis)
        self.replace_label(self.inspect_cast, selected_film.cast)
        self.replace_label(self.inspect_genres, selected_film.string_conv("genres"))

    def resize(self, event):
        """Listens to configure events on this window.

        Detects if window size has changed and uses this data to adjust
        where labels/text should wrap."""
        # Was this event spawned by the root window?
        if type(event.widget) != type(self.master):
            return

        if (self.window_width == event.width) and (self.window_height == event.height):
            return

        wraplength = event.width - 10

        self.inspect_title.configure(wraplength=wraplength)
        self.inspect_synopsis.configure(wraplength=wraplength)
        self.inspect_cast.configure(wraplength=wraplength)
        self.inspect_genres.configure(wraplength=wraplength)

        self.window_width = event.width
        self.window_height = event.height

    def add_film(self):
        """Callback for add button."""
        new_film = self.master.show_modal(FilmEditWindow, {"edit_type": FilmEditWindow.ADD})
        if not new_film:
            return

        self.treeview_insert(new_film)
        self.treeview_sort()

    def delete_film(self):
        """Callback for delete button."""
        selected_id = int(self.treeview.selection()[0])

        selected_film = session.query(Film).get(selected_id)
        if not selected_film:  # This shouldn't happen, but we can't continue if it somehow does
            return

        confirm = messagebox.askyesno(
            message=f"Are you sure you want to delete the film '{selected_film.title}'?",
            title="Delete", icon="question")

        if not confirm:
            return

        session.delete(selected_film)
        session.commit()
        self.treeview.delete(str(selected_id))

        # film deleted -> selection cleared, so delete and update buttons need to be disabled again
        self.delete_film_button.state(["disabled"])
        self.update_film_button.state(["disabled"])

        # Clear inspect section data
        self.replace_label(self.inspect_title, "")
        self.replace_label(self.inspect_year, "")
        self.replace_label(self.inspect_rating, "")
        self.replace_label(self.inspect_age_rating, "")
        self.replace_label(self.inspect_duration, "")
        self.replace_label(self.inspect_synopsis, "")
        self.replace_label(self.inspect_cast, "")
        self.replace_label(self.inspect_genres, "")

    def update_film(self):
        """Callback for update button."""
        selected_id = int(self.treeview.selection()[0])

        film = session.query(Film).get(selected_id)
        if not film:
            return

        self.master.show_modal(FilmEditWindow, {
            "edit_type": FilmEditWindow.EDIT,
            "film": film
        })

        # Update item in tree with new values
        iid = str(film.id)

        h, m = get_hours_minutes(film.duration.total_seconds())

        self.treeview.set(iid, 0, film.title)
        self.treeview.set(iid, 1, film.year_published)
        self.treeview.set(iid, 2, film.age_rating.value)
        self.treeview.set(iid, 3, film.string_conv("duration"))
        self.treeview.set(iid, 4, film.string_conv("rating"))

        # Sort tree incase title changed
        self.treeview_sort()

        # Update inspect section data
        self.inspected_film_id = None
        self.treeview_select(None)

    def view_film_showings(self):
        """Callback for view showings button."""
        pass