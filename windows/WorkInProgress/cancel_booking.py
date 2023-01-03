from tkinter import ttk
from database_models import session, Showing, Cinema, Film, Screen, Genre, AgeRatings, Booking
from windows import FilmShowingWindow, FilmWindow

#Alchemy code here

class cancelBooking(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)
        
        self.inspect_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=1000, height=1000)
        #Booking reference field
        self.booking_reference = ttk.Entry(self.inspect_frame, width= 20, textvariable="Booking Reference: ")
        #Surname field
        self.booking_surname = ttk.Entry(self.inspect_frame, width= 20, textvariable="Surname: ")
        #Validation before searching database
        self.confirm_button = ttk.Button(self.inspect_frame, text="Confirm")
        #Cancel booking button
        self.cancel_button = ttk.Button(self.inspect_frame, text="Cancel Booking", image=parent.delete_icon, compund="left")
        #Deletes booking from database

        self.booking_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=1000, height=1000)
        # Pull data from db and show booking that matches booking reference
        self.booking_data = ttk.Label(self.booking_data, text="booking details here")

        # --- Gridding ---
        self.inspect_frame.grid(column=0, row=0, rowspan=3, sticky="nsew")
        self.booking_reference.grid(column=0, row=0)
        self.booking_surname.grid(column=0, row=1)
        self.confirm_button.grid(column=1, row=1, sticky="se")
        self.cancel_button.grid(column=0, row=2, sticky="s")

        self.booking_frame.grid(column=1, row=0, rowspan=3, sticky="nsew")
        self.booking_data.grid(column=1, row=0)

        for i in range(3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(2, weight=1)