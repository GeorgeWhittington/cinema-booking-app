from io import BytesIO

from cairosvg import svg2png
from tkinter import ttk
from PIL import ImageTk, Image

from database_models import session_scope, Film


class FilmWindow(ttk.Frame):
    """Window which allows for Admins and Managers to: inspect, add, update and delete films."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # TODO: Get rid of headings and just stick back to listings button on topmost row?
        self.heading_1 = ttk.Label(self, text="All Films")
        self.heading_1.grid(column=0, row=0)

        self.heading_2 = ttk.Label(self, text="More Details")
        self.heading_2.grid(column=1, row=0)

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
        for i, value in enumerate(headings):
            self.treeview.heading(i, text=value)
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

        self.treeview.grid(column=0, row=1, sticky="nsew")
        self.inspected_film_id = None

        self.inspect_frame = ttk.Frame(self)
        self.inspect_frame.grid(column=1, row=1, sticky="nsew")

        self.inspect_title = ttk.Label(self.inspect_frame, text="Title:")
        self.inspect_year = ttk.Label(self.inspect_frame, text="Year Published:")
        self.inspect_rating = ttk.Label(self.inspect_frame, text="Rating:")
        self.inspect_age_rating = ttk.Label(self.inspect_frame, text="Age Rating:")
        self.inspect_duration = ttk.Label(self.inspect_frame, text="Duration:")
        self.inspect_synopsis = ttk.Label(self.inspect_frame, wraplength=400, text="Synopsis:")
        self.inspect_cast = ttk.Label(self.inspect_frame, text="Cast:")
        
        for y, widget in enumerate([self.inspect_title, self.inspect_year, self.inspect_rating, self.inspect_age_rating, self.inspect_duration, self.inspect_synopsis, self.inspect_cast]):
            widget.grid(column=0, row=y, sticky="w")

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(column=0, row=2, sticky="nsew")

        # for x in range(4):
        #     self.button_frame.columnconfigure(x, weight=1)

        out = BytesIO()
        svg2png(url="assets/plus-solid.svg", write_to=out)
        self.add_icon = ImageTk.PhotoImage(Image.open(out).resize((15, 15)))
        self.add_film_button = ttk.Button(
            self.button_frame, text="Add", image=self.add_icon,
            compound="left", command=self.add_film)
        self.add_film_button.grid(column=0, row=0)

        out = BytesIO()
        svg2png(url="assets/trash-solid.svg", write_to=out)
        self.delete_icon = ImageTk.PhotoImage(Image.open(out).resize((15, 15)))
        self.delete_film_button = ttk.Button(
            self.button_frame, text="Delete", image=self.delete_icon,
            compound="left", command=self.delete_film)
        self.delete_film_button.state(["disabled"])  # Requires a selection to work, begins disabled
        self.delete_film_button.grid(column=1, row=0)

        out = BytesIO()
        svg2png(url="assets/pen-solid.svg", write_to=out)
        self.update_icon = ImageTk.PhotoImage(Image.open(out).resize((15, 15)))
        self.update_film_button = ttk.Button(
            self.button_frame, text="Update", image=self.update_icon,
            compound="left", command=self.update_film)
        self.update_film_button.state(["disabled"])  # Requires a selection to work, begins disabled
        self.update_film_button.grid(column=2, row=0)

        out = BytesIO()
        svg2png(url="assets/eye-solid.svg", write_to=out)
        self.view_icon = ImageTk.PhotoImage(Image.open(out).resize((15, 15)))
        self.view_showings_button = ttk.Button(
            self.button_frame, text="View Showings", image=self.view_icon,
            compound="left", command=self.view_film_showings)
        self.view_showings_button.grid(column=3, row=0)

        for x in range(4):
            self.columnconfigure(x, weight=1)

    @staticmethod
    def replace_label(label, new_value):
        current_text = label["text"]
        # We only care about splitting to get the data before the first ':'
        key, _ = current_text.split(":", maxsplit=1)
        label.config(text=f"{key}: {new_value}")

    def treeview_select(self, event):
        if not self.inspected_film_id:
            # A selection has been made, so these buttons can be enabled
            self.delete_film_button.state(["!disabled"])
            self.update_film_button.state(["!disabled"])

        selected_id = int(self.treeview.selection()[0])
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
    
    def add_film(self):
        pass

    def delete_film(self):
        pass

    def update_film(self):
        pass

    def view_film_showings(self):
        pass