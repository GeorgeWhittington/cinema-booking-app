from tkinter import ttk
from database_models import session, Showing, Cinema, Film, Screen, Genre, AgeRatings, Booking
from windows import FilmShowingWindow, FilmWindow

class cancelBooking(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)
        
        self.inspect_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=1000, height=1000)
        #Treeview of each cinema locations
        
        #add button
        self.add_loc_button = ttk.Button(self.inspect_frame, text="Add Location")
        #brings up entry field to add data to db

        #edit button
        self.edit_loc_button = ttk.Button(self.inspect_frame, text="Edit Location")
        #entry field to edit data in db

        #remove button
        self.delete_loc_button = ttk.Button(self.inspect_frame, text="Delete Location")
        #clears data from db

        # --- Gridding ---
        self.inspect_frame.grid(column=0, row=0, rowspan=3, sticky="nsew")
        self.add_loc_button.grid(column=0, row=1)
        self.edit_loc_button.grid(column=1, row=1)
        self.delete_loc_button.grid(column=2, row=1)