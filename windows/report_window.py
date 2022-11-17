from datetime import datetime
from calendar import monthrange, month_name

from fpdf import FPDF
from tkinter import ttk, Listbox, StringVar, messagebox, filedialog
from sqlalchemy.sql import func, asc, desc, and_
from prettytable import PrettyTable

from database_models import session, Film, Showing, Booking, Cinema, Screen, User
from misc import FILM_FORMAT


class ReportWindow(ttk.Frame):
    REPORT_TYPES = {
        "BOOKINGS_PER_FILM": "Total number of bookings per film",
        "MONTHLY_REVENUE": "Total monthly revenue for each cinema",
        "TOP_REVENUE": "Top revenue generating film",
        "EMPLOYEE_BOOKINGS": "Monthly total of bookings each employee has made"
    }

    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        self.report_type_listbox = Listbox(self, listvariable=StringVar(value=list(ReportWindow.REPORT_TYPES.values())))
        self.report_type_listbox.bind("<<ListboxSelect>>", self.report_select)

        self.generate_button = ttk.Button(self, text="Generate Report", command=self.generate_report)
        self.generate_button.state(["disabled"])  # Requires selection to work, begins disabled

        self.report_type_listbox.grid(column=0, row=0, sticky="nesw")
        self.generate_button.grid(column=0, row=1, sticky="sew")

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    def report_select(self, event):
        """Enables the generate button when a selection is first made."""
        try:
            selected = int(self.report_type_listbox.curselection()[0])
        except IndexError:
            return

        self.generate_button.state(["!disabled"])

    @staticmethod
    def get_month_start_end(month, year):
        month_start = datetime(year=year, month=month, day=1)
        _, month_length = monthrange(year, month)
        month_end = datetime(year=year, month=month, day=month_length, hour=23, minute=59, second=59)

        return month_start, month_end

    def save_to_pdf(self, title, table, default_filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "", 18)
        pdf.write(txt=title)
        pdf.ln(h=10)
        pdf.set_font("courier", "", 10)
        pdf.write(txt=table)

        filename = filedialog.asksaveasfilename(initialfile=default_filename, defaultextension="pdf")
        if not filename:
            return

        pdf.output(filename)

    def generate_report(self):
        try:
            selected = int(self.report_type_listbox.curselection()[0])
        except IndexError:
            messagebox.showerror(title="Error", message="Please select a report to generate")
            self.generate_button.state(["disabled"])
            return

        selected = list(ReportWindow.REPORT_TYPES.values())[selected]

        if selected == ReportWindow.REPORT_TYPES["BOOKINGS_PER_FILM"]:
            """The equivalent sql for this sqlalchemy query:

            SELECT
                *,
                SUM(booking.lower_booked) AS `lb`,
                SUM(booking.upper_booked) AS `ub`,
                SUM(booking.vip_booked) AS `vb`,
                (`lb` + `ub` + `vb`) AS `total_b`
            FROM film
            INNER JOIN showing ON film.id = showing.film_id
            INNER JOIN booking ON showing.id = booking.showing_id
            GROUP BY film.id
            ORDER BY DESC `total_b`"""
            lower = func.sum(Booking.lower_booked)
            upper = func.sum(Booking.upper_booked)
            vip = func.sum(Booking.vip_booked)

            query = session.query(Film, lower, upper, vip, (lower + upper + vip).label("total_b"))
            query = query.join(Film.showings).join(Showing.bookings).group_by(Film.id)
            query = query.order_by(desc("total_b"))

            table = PrettyTable()
            table.field_names = ["Film", "Lower Hall", "Upper Gallery", "VIP", "Total"]
            for film, *booking_values in query.all():
                table.add_row([FILM_FORMAT.format(film), *booking_values])

            self.save_to_pdf(title=selected, table=table.get_string(), default_filename="bookings per film")
        elif selected == ReportWindow.REPORT_TYPES["MONTHLY_REVENUE"]:
            try:
                month, year = self.master.show_modal(ReportDateDialog)
            except TypeError:
                # User closed datepicker without selecting, cancel report generation
                return
            month_start, month_end = self.get_month_start_end(month, year)

            cinemas = session.query(Cinema).all()

            for cinema in cinemas:
                query = session.query(Showing).join(Showing.screen)
                query = query.filter(Screen.cinema == cinema).filter(and_(
                    Showing.show_time >= month_start,
                    Showing.show_time <= month_end))

                cinema.total_revenue = 0.0

                for showing in query.all():
                    cinema.total_revenue += sum([booking.calculate_price() for booking in showing.bookings])

                cinema.total_revenue = round(cinema.total_revenue, 2)

            cinemas = sorted(cinemas, key=lambda c: c.total_revenue, reverse=True)

            table = PrettyTable(custom_format={"Total Revenue": lambda f, v: f'£{v:.2f}'})
            table.field_names = ["Cinema", "Total Revenue"]
            table.add_rows([cinema.name, cinema.total_revenue] for cinema in cinemas)

            self.save_to_pdf(
                title=f"Total revenue for {month_start.strftime('%B %Y')}",
                table=table.get_string(),
                default_filename=f"cinema revenue {month_start.strftime('%B %Y')}")
        elif selected == ReportWindow.REPORT_TYPES["TOP_REVENUE"]:
            films = session.query(Film).all()

            for film in films:
                film.total_revenue = 0.0

                for showing in film.showings:
                    film.total_revenue += sum([booking.calculate_price() for booking in showing.bookings])

                film.total_revenue = round(film.total_revenue, 2)

            films = sorted(films, key=lambda f: f.total_revenue, reverse=True)

            film_string = FILM_FORMAT.format(films[0])
            self.save_to_pdf(
                title=selected,
                table=f"{film_string} has generated a total of £{films[0].total_revenue:.2f}",
                default_filename="top revenue film")
        elif selected == ReportWindow.REPORT_TYPES["EMPLOYEE_BOOKINGS"]:
            try:
                month, year = self.master.show_modal(ReportDateDialog)
            except TypeError:
                # User closed datepicker without selecting, cancel report generation
                return
            month_start, month_end = self.get_month_start_end(month, year)

            """Equivalent sql for this query is:

            SELECT
                *,
                COUNT(booking.id) AS `booking_count`
            FROM user
            INNER JOIN booking ON user.id = booking.employee_id
            INNER JOIN showing ON booking.showing_id = showing.id
            WHERE
                showing.show_time >= {month_start} AND
                showing.show_time <= {month_end}
            GROUP BY user.id
            ORDER BY DESC `booking_count`"""
            query = session.query(User, func.count(Booking.id).label("booking_count"))
            query = query.join(User.bookings).join(Booking.showing)
            query = query.filter(and_(
                    Showing.show_time >= month_start,
                    Showing.show_time <= month_end))
            query = query.group_by(User.id).order_by(desc("booking_count"))

            table = PrettyTable()
            table.field_names = ["Employee", "Total Bookings"]
            table.add_rows([user.username, total_bookings] for user, total_bookings in query.all())

            self.save_to_pdf(
                title=f"Total bookings per employee for {month_start.strftime('%B %Y')}",
                table=table.get_string(),
                default_filename=f"employee bookings {month_start.strftime('%B %Y')}")


class ReportDateDialog(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.dismiss = kwargs.pop("dismiss")
        super().__init__(parent, *args, **kwargs)

        self.month_combobox = ttk.Combobox(self)
        self.month_combobox["values"] = list(month_name)
        self.month_combobox.state(["readonly"])

        earliest_showing = session.query(Showing).order_by(asc(Showing.show_time)).first()
        today = datetime.now()

        self.year_combobox = ttk.Combobox(self)
        self.year_combobox["values"] = list(range(earliest_showing.show_time.year, today.year + 1))
        self.year_combobox.state(["readonly"])

        self.select_button = ttk.Button(self, text="Select Month", command=self.select)

        self.month_combobox.grid(column=0, row=0)
        self.year_combobox.grid(column=1, row=0)
        self.select_button.grid(column=0, row=1, columnspan=2)

        self.month_combobox.set(today.strftime("%B"))
        self.year_combobox.set(today.year)

    def select(self):
        month = list(month_name).index(self.month_combobox.get())
        year = int(self.year_combobox.get())

        self.result = (month, year)
        self.dismiss()