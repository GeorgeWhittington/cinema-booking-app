from tkinter import ttk
from database_models import session, Showing, Cinema, Film, Screen, Genre, AgeRatings, Booking
from windows import FilmShowingWindow, FilmWindow

class cancelBooking(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)
        
        self.inspect_frame = ttk.Frame(self)
        #Booking reference field
        self.booking_reference = ttk.Entry(self.inspect_frame, textvariable="Booking Reference:")
        self.cancel_button = ttk.Button(self.inspect_frame, text="Cancel Booking", image=parent.delete_icon, compund="left")

        self.booking = session.query(Booking).filter_by(Booking.id).first()
        session.delete(Booking)
        session.commit()

        # --- Gridding ---
        self.inspect_frame.grid(column=0, row=0, rowspan=3, sticky="nsew")
        self.booking_reference.grid(column=0, row=0)
        self.cancel_button.grid(column=0, row=1, sticky="s")