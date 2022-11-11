import re
from tkinter import ttk, messagebox

from sqlalchemy.sql import func

from database_models import session, Showing, Booking, Cinema, Film, Screen

film_regex = re.compile(r"(?P<title>.*) \((?P<year_published>\d{4})\)")


class FilmShowingWindow(ttk.Frame):
    """Window which allows admins/managers to view and edit Film Showings."""
    def __init__(self, parent, *args, **kwargs):
        self.film_filter = kwargs.pop("film_filter", None)
        self.cinema_filter = kwargs.pop("cinema_filter", None)

        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        # Widget creation
        headings = [
            "Film",
            "Cinema",
            "Screen",
            "Show Time"
        ]

        self.treeview = ttk.Treeview(self,
            columns=tuple(i for i in range(len(headings))),
            show="headings",
            selectmode="browse")  # Only allow one row to be selected at once
        self.treeview_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview["yscrollcommand"] = self.treeview_scrollbar.set
        for i, value in enumerate(headings):
            self.treeview.column(i, stretch=True)
            self.treeview.heading(i, text=value)

        self.treeview.bind("<<TreeviewSelect>>", self.treeview_select)

        self.populate_treeview()

        self.filter_frame = ttk.LabelFrame(self, text="Filters")

        self.cinema_label = ttk.Label(self.filter_frame, text="Cinema")
        self.cinema_combobox = ttk.Combobox(self.filter_frame)
        self.cinema_combobox["values"] = ["- All Cinemas -"] + [cinema.name for cinema in session.query(Cinema).all()]
        self.cinema_combobox.state(["readonly"])
        if self.cinema_filter:
            cinema = session.query(Cinema).get(self.cinema_filter)
            self.cinema_combobox.set(cinema.name)
        else:
            self.cinema_combobox.set("- All Cinemas -")
        self.cinema_combobox.bind("<<ComboboxSelected>>", self.cinema_filter_change)

        self.film_label = ttk.Label(self.filter_frame, text="Film")
        self.film_combobox = ttk.Combobox(self.filter_frame)
        self.film_combobox["values"] = ["- All Films -"] + [f"{film.title} ({film.year_published})" for film in session.query(Film).all()]
        self.film_combobox.state(["readonly"])
        if self.film_filter:
            film = session.query(Film).get(self.film_filter)
            self.film_combobox.set(f"{film.title} ({film.year_published})")
        else:
            self.film_combobox.set("- All Films -")
        self.film_combobox.bind("<<ComboboxSelected>>", self.film_filter_change)

        self.button_frame = ttk.Frame(self)

        self.add_showing_button = ttk.Button(
            self.button_frame, text="Add", image=parent.add_icon,
            compound="left", command=self.add_showing)

        self.delete_showing_button = ttk.Button(
            self.button_frame, text="Delete", image=parent.delete_icon,
            compound="left", command=self.delete_showing)
        self.delete_showing_button.state(["disabled"])  # Requires a selection to work, begins disabled

        self.update_showing_button = ttk.Button(
            self.button_frame, text="Update", image=parent.update_icon,
            compound="left", command=self.update_showing)
        self.update_showing_button.state(["disabled"])  # Requires a selection to work, begins disabled

        # Gridding
        self.treeview.grid(column=0, row=0, sticky="nsew")
        self.treeview_scrollbar.grid(column=1, row=0, sticky="ns")

        self.filter_frame.grid(column=2, row=0, sticky="nsew")

        self.cinema_label.grid(column=0, row=0, sticky="w")
        self.cinema_combobox.grid(column=0, row=1, sticky="ew")

        self.film_label.grid(column=0, row=2, sticky="w")
        self.film_combobox.grid(column=0, row=3, sticky="ew")

        self.button_frame.grid(column=0, row=1, columnspan=3, sticky="nsew")

        self.add_showing_button.grid(column=0, row=0)
        self.delete_showing_button.grid(column=1, row=0)
        self.update_showing_button.grid(column=2, row=0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, minsize=230, weight=0)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    def populate_treeview(self):
        self.treeview.delete(*self.treeview.get_children())

        for showing in self.film_showing_query():
            start = showing.show_time
            end = showing.show_time + showing.film.duration

            self.treeview.insert(
                "", "end", iid=showing.id,
                values=(
                    f"{showing.film.title} ({showing.film.year_published})",
                    showing.screen.cinema.name,
                    showing.screen.name,
                    f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"))

    def film_showing_query(self):
        query = session.query(Showing).join(Showing.screen).join(Screen.cinema).order_by(Cinema.name, Screen.name)

        if self.film_filter:
            query = query.join(Showing.film).filter(Film.id == self.film_filter)

        if self.cinema_filter:
            query = query.filter(Cinema.id == self.cinema_filter)

        return query.all()

    def treeview_select(self, event):
        pass

    def cinema_filter_change(self, event):
        filter_value = self.cinema_combobox.get()

        if filter_value == "- All Cinemas -":
            self.cinema_filter = None
            self.populate_treeview()
            return

        cinema = session.query(Cinema).filter_by(name=filter_value).first()

        if self.cinema_filter == cinema.id:
            return

        self.cinema_filter = cinema.id
        self.populate_treeview()

    def film_filter_change(self, event):
        filter_value = self.film_combobox.get()

        if filter_value == "- All Films -":
            self.film_filter = None
            self.populate_treeview()
            return

        match = film_regex.match(filter_value)
        film = session.query(Film).filter_by(
            title=match.group("title"),
            year_published=match.group("year_published")).first()

        if self.film_filter == film.id:
            return

        self.film_filter = film.id
        self.populate_treeview()

    def add_showing(self):
        pass

    def delete_showing(self):
        pass

    def update_showing(self):
        pass