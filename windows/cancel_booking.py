from tkinter import ttk, messagebox

from database_models import session, Showing, Cinema, Film, Screen, Genre, AgeRatings, Booking
from windows import FilmShowingWindow, FilmWindow

class cancelBooking(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        #Booking reference field
        self.booking_ref_label = ttk.Label(self, text="Booking Reference:")
        self.booking_reference = ttk.Entry(self)

        self.cancel_button = ttk.Button(self,
            text="Cancel Booking", image=parent.delete_icon, compound="left", command=self.cancel_pressed)

        self.booking_ref_label.grid(column=0, row=0)
        self.booking_reference.grid(column=1, row=0)
        self.cancel_button.grid(column=0, row=1, columnspan=2)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def cancel_pressed(self):
        booking_id = self.booking_reference.get().strip()

        booking = session.query(Booking).get(booking_id)
        if not booking:
            messagebox.showerror(
                title="Invalid Booking Reference",
                message=f"The booking #{booking_id} does not exist")
            return

        response = messagebox.askyesno(title="Are you sure?",
            message=f"Are you sure you want to cancel the booking #{booking.id} for {booking.name} seeing {booking.showing.film.title}?")

        if response:
            session.delete(booking)
            session.commit()