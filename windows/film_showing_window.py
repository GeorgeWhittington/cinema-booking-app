import re
from datetime import datetime, time

from tkinter import ttk, messagebox, font
from tkcalendar import Calendar

from database_models import session, Showing, Cinema, Film, Screen
from misc.constants import ADD, EDIT

film_regex = re.compile(r"(?P<title>.*) \((?P<year_published>\d{4})\)")
film_format = "{0.title} ({0.year_published})"
midnight = time(hour=0, minute=0)
eight_am = time(hour=8, minute=0)


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
        self.film_combobox["values"] = ["- All Films -"] + [film_format.format(film) for film in session.query(Film).all()]
        self.film_combobox.state(["readonly"])
        if self.film_filter:
            film = session.query(Film).get(self.film_filter)
            self.film_combobox.set(film_format.format(film))
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

        self.update_showing_button = ttk.Button(
            self.button_frame, text="Update", image=parent.update_icon,
            compound="left", command=self.update_showing)

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

        # Needs to happen last so that buttons exist
        self.populate_treeview()

    def populate_treeview(self):
        """Clears the treeview and then refills it with all the showings
        that match the currently selected filters."""
        self.treeview.delete(*self.treeview.get_children())

        # Contents have changed, so selection is cleared, disable buttons that require one
        self.delete_showing_button.state(["disabled"])
        self.update_showing_button.state(["disabled"])

        for showing in self.film_showing_query():
            start = showing.show_time
            end = showing.show_time + showing.film.duration

            self.treeview.insert(
                "", "end", iid=showing.id,
                values=(
                    film_format.format(showing.film),
                    showing.screen.cinema.name,
                    showing.screen.name,
                    f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"))

    def film_showing_query(self):
        """Generates and executes a query collecting all film
        showings that match the current filters."""
        query = session.query(Showing).join(Showing.screen).join(Screen.cinema)
        query = query.order_by(Cinema.name, Screen.name)

        if self.film_filter:
            query = query.join(Showing.film).filter(Film.id == self.film_filter)

        if self.cinema_filter:
            query = query.filter(Cinema.id == self.cinema_filter)

        return query.all()

    def treeview_select(self, event):
        """Listens to the selection event on the treeview,
        uses this data to enable the update/delete buttons."""
        try:
            selected_id = int(self.treeview.selection()[0])
        except IndexError:
            return

        self.delete_showing_button.state(["!disabled"])
        self.update_showing_button.state(["!disabled"])

    def cinema_filter_change(self, event):
        """Listens to the selection event on the cinema_combobox element.

        If it changes the cinema_filter value is updated and the treeview
        is repopulated."""
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
        """Listens to the selection event on the film_combobox element.

        If it changes the film_filter value is updated and the treeview
        is repopulated."""
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

    def check_selection(self):
        try:
            selected_id = int(self.treeview.selection()[0])
            return selected_id
        except IndexError:
            messagebox.showerror(title="Error", message="No showing selected")
            self.delete_showing_button.state(["disabled"])
            self.update_showing_button.state(["disabled"])

    def check_showing_exists(self, showing_id):
        showing = session.query(Showing).get(showing_id)
        if not showing:
            # Shouldn't happen, but repopulate treeview to fix it if it does
            messagebox.showerror(title="Error", message="That showing no longer exists")
            self.populate_treeview()
        else:
            return showing

    def add_showing(self):
        self.master.show_modal(FilmShowingEditDialog, {"edit_type": ADD})

    def delete_showing(self):
        if not (selected_id := self.check_selection()):
            return

        if not (showing := self.check_showing_exists(selected_id)):
            return

        film_string = film_format.format(showing.film)
        choice = messagebox.askyesno(
            title="Delete", icon="question",
            message=f"Are you sure you want to delete this showing of {film_string} at {showing.screen.cinema.name}?")

        if not choice:
            return

        session.delete(showing)
        session.commit()

        self.populate_treeview()

    def update_showing(self):
        if not (selected_id := self.check_selection()):
            return

        if not (showing := self.check_showing_exists(selected_id)):
            return

        self.master.show_modal(FilmShowingEditDialog, {
            "edit_type": EDIT,
            "showing": showing
        })

        # pop up add/delete dialog
        # if it's result is True something has changed, so run self.populate_treeview()


class FilmShowingEditDialog(ttk.Frame):
    """Dialog for adding or updating Film Showings.

    if 'edit_type' is EDIT then the kwarg 'showing' needs to be set
    to the showing being edited"""
    def __init__(self, parent, *args, **kwargs):
        self.dismiss = kwargs.pop("dismiss")
        self.edit_type = kwargs.pop("edit_type")

        if self.edit_type == ADD:
            parent.title("Add Film Showing")
        elif self.edit_type == EDIT:
            self.showing = kwargs.pop("showing")
            parent.title("Edit Film Showing")

        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        # Widget Creation
        self.film_label = ttk.Label(self, text="Film:")
        self.cinema_label = ttk.Label(self, text="Cinema:")
        self.screen_label = ttk.Label(self, text="Screen:")
        self.show_date_label = ttk.Label(self, text="Show Date:")
        self.show_time_label = ttk.Label(self, text="Show Time:")

        self.film_combobox = ttk.Combobox(self)
        self.film_combobox["values"] = [film_format.format(film) for film in session.query(Film).order_by(Film.title, Film.year_published).all()]
        self.film_combobox.state(["readonly"])
        self.film_combobox.bind("<<ComboboxSelected>>", self.recalc_show_end)

        self.cinema_combobox = ttk.Combobox(self)
        self.cinema_combobox["values"] = [cinema.name for cinema in session.query(Cinema).order_by(Cinema.name).all()]
        self.cinema_combobox.state(["readonly"])
        self.cinema_combobox.bind("<<ComboboxSelected>>", self.cinema_selected)

        self.screen_combobox = ttk.Combobox(self)
        self.screen_combobox.state(["readonly", "disabled"])

        self.show_date_frame = ttk.Frame(self)
        self.show_date_data_label = ttk.Label(self.show_date_frame)
        self.show_date_calendar = Calendar(self.show_date_frame,
            locale="en_GB", background="white", foreground="black",
            showweeknumbers=False, selectforeground="blue",
            font=font.BOLD)
        self.show_date_calendar.bind("<<CalendarSelected>>", self.calendar_selected)

        self.show_time_frame = ttk.Frame(self)

        self.show_time_spinbox_hour = ttk.Spinbox(self.show_time_frame, from_=8, to=23, format="%02.0f", width=2)
        self.show_time_spinbox_hour.state(["readonly"])
        self.show_time_spinbox_hour.bind("<ButtonRelease-1>", self.spinbox_change)

        self.show_time_label_1 = ttk.Label(self.show_time_frame, text=":")

        self.show_time_spinbox_minute = ttk.Spinbox(self.show_time_frame, from_=0, to=59, format="%02.0f", width=2)
        self.show_time_spinbox_minute.state(["readonly"])
        self.show_time_spinbox_minute.bind("<ButtonRelease-1>", self.spinbox_change)

        self.show_time_label_2 = ttk.Label(self.show_time_frame, text="to")
        self.show_time_label_3 = ttk.Label(self.show_time_frame, text="--:--")

        self.button_frame = ttk.Frame(self)
        self.submit_button = ttk.Button(self.button_frame, text=self.edit_type, command=self.submit)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.dismiss)

        # Gridding
        widgets = [
            (self.film_label, self.film_combobox),
            (self.cinema_label, self.cinema_combobox),
            (self.screen_label, self.screen_combobox),
            (self.show_date_label, self.show_date_frame),
            (self.show_time_label, self.show_time_frame)
        ]

        for y, (label, combobox) in enumerate(widgets):
            if y == 3:
                label.grid(column=0, row=y, pady=2, sticky="nw")
            else:
                label.grid(column=0, row=y, pady=2, sticky="w")
            combobox.grid(column=1, row=y, pady=2, sticky="ew")

        self.show_date_data_label.grid(column=0, row=0)
        self.show_date_calendar.grid(column=0, row=1)

        self.show_time_spinbox_hour.grid(column=0, row=0)
        self.show_time_label_1.grid(column=1, row=0)
        self.show_time_spinbox_minute.grid(column=2, row=0)
        self.show_time_label_2.grid(column=3, row=0)
        self.show_time_label_3.grid(column=4, row=0)

        self.button_frame.grid(column=0, row=len(widgets), columnspan=2)
        self.submit_button.grid(column=0, row=0)
        self.cancel_button.grid(column=1, row=0)

        if self.edit_type == ADD:
            self.show_date_data_label["text"] = self.show_date_calendar.get_date()
            self.show_time_spinbox_hour.set("08")
            self.show_time_spinbox_minute.set("00")
        elif self.edit_type == EDIT:
            self.film_combobox.set(film_format.format(self.showing.film))
            self.cinema_combobox.set(self.showing.screen.cinema.name)

            self.cinema_selected(None)

            self.screen_combobox.set(self.showing.screen.name)
            self.show_date_calendar.selection_set(self.showing.show_time)
            self.show_time_spinbox_hour.set(self.showing.show_time.strftime("%H"))
            self.show_time_spinbox_minute.set(self.showing.show_time.strftime("%M"))

            self.recalc_show_end(None)

    def cinema_selected(self, event):
        """When a cinema is selected the list of screens available to
        choose from is updated."""
        cinema = session.query(Cinema).filter_by(name=self.cinema_combobox.get()).first()
        if not cinema:
            return  # Shouldn't happen

        screens = [screen.name for screen in
            session.query(Screen).filter_by(cinema=cinema).order_by(Screen.name).all()]
        self.screen_combobox["values"] = screens
        self.screen_combobox.set("")  # Clear old selection

        if screens:
            self.screen_combobox.state(["!disabled"])
        else:
            self.screen_combobox.state(["disabled"])

    def calendar_selected(self, event):
        """Tracks calendar updates to update the date label and trigger
        show end time updates for the rare edge cases where date effects time,
        eg: clocks going back."""
        self.show_date_data_label["text"] = self.show_date_calendar.get_date()
        self.recalc_show_end(None)

    def spinbox_change(self, event):
        """Spinboxes have a small delay between events that signal
        they have changed, and their value updating. To counter this
        calls to recalc_show_end from them are delayed slightly too."""
        # 1ms
        self.after(1, self.recalc_show_end, None)

    def recalc_show_end(self, event):
        """Called whenever something to do with show time is changed,
        the show end time is updated using this new data."""
        self.show_date_data_label["text"] = self.show_date_calendar.get_date()
        selected_date = self.show_date_calendar.selection_get()

        match = film_regex.match(self.film_combobox.get())

        if not match:
            return

        film = session.query(Film).filter_by(
            title=match.group("title"),
            year_published=match.group("year_published")).first()

        if not film:
            return  # Shouldn't be possible

        try:
            hour = int(self.show_time_spinbox_hour.get())
            minute = int(self.show_time_spinbox_minute.get())
        except ValueError:
            return

        # timedelta addition requires datetime object, comparisons further down
        # require time objects, hence 4 different values
        start_time = time(hour=hour, minute=minute)
        start_datetime = datetime.combine(selected_date, start_time)
        end_datetime = film.duration + start_datetime
        end_time = time(hour=end_datetime.hour, minute=end_datetime.minute)

        self.show_time_label_3["text"] = end_datetime.strftime("%H:%M")

        if start_time > midnight and start_time < eight_am or\
                end_time > midnight and end_time < eight_am:
            # starts or ends during closed hours, not a valid showtime
            self.show_time_label_3.config({"foreground": "red"})
        else:
            self.show_time_label_3.config({"foreground": "black"})

    def submit(self):
        pass