from datetime import datetime
from calendar import monthrange

from tkinter import ttk, Listbox, StringVar, messagebox
from sqlalchemy.sql import func, desc, and_
from prettytable import PrettyTable

from database_models import session, Film, Showing, Booking, Cinema, Screen


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

    def generate_report(self):
        try:
            selected = int(self.report_type_listbox.curselection()[0])
        except IndexError:
            messagebox.showerror(title="Error", message="Please select a report to generate")
            self.generate_button.state(["disabled"])
            return

        selected = list(ReportWindow.REPORT_TYPES.values())[selected]

        if selected == ReportWindow.REPORT_TYPES["BOOKINGS_PER_FILM"]:
            lower = func.sum(Booking.lower_booked).label("lb")
            upper = func.sum(Booking.upper_booked).label("ub")
            vip = func.sum(Booking.vip_booked).label("vb")

            query = session.query(Film, lower, upper, vip, (lower + upper + vip).label("total_b"))
            query = query.join(Film.showings).join(Showing.bookings).group_by(Film.id)
            query = query.order_by(desc("total_b"))

            table = PrettyTable()
            table.field_names = ["Film", "Lower Hall", "Upper Gallery", "VIP", "Total"]
            for film, *booking_values in query.all():
                table.add_row([f"{film.title} ({film.year_published})", *booking_values])

            # Obviously temporary, but PrettyTable can output html
            # so table -> html -> pdf workflow could be possible?
            print(selected)
            print(table)
        elif selected == ReportWindow.REPORT_TYPES["MONTHLY_REVENUE"]:
            # This should be an option the user is provided with via popup
            today = datetime.now()
            month_start = datetime(year=today.year, month=today.month, day=1)
            _, month_length = monthrange(today.year, today.month)
            month_end = datetime(year=today.year, month=today.month, day=month_length, hour=23, minute=59, second=59)

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

            print(f"Total revenue for {month_start.strftime('%B %Y')}")
            print(table)