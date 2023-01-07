from enum import Enum
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
from sqlalchemy import Column, Float, Integer, Interval, String, Text

from sqlalchemy.sql import and_
from datetime import datetime, time
from misc.constants import ADD, EDIT, FILM_FORMAT, MIDNIGHT, EIGHT_AM

from database_models import session, Showing, Cinema, Film, Screen, Genre, AgeRatings
from windows import FilmShowingWindow, FilmWindow


class enterDetails(ttk.Frame):
    def __init__(self, filepath, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        #To enter details for booking
        self.details_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=1000, height=1000)
        self.details_title = ttk.LabelFrame(self.details_frame, text="Booking Details")
        self.first_name_label = ttk.Label(self.details_frame, text="First Name:")
        self.first_name_field = ttk.Entry(self.details_frame)

        self.surname_label = ttk.Label(self.details_frame, text="Last Name:")
        self.surname_field = ttk.Entry(self.details_frame)

        self.name_label = ttk.Label(self.details_frame, text="Full Name:")
        self.name_field = ttk.Entry(self.details_frame)

        self.seating_option = ttk.Label(self.details_frame, text="Seating Area")
        self.seating_field = tk.StringVar(self.details_frame)
        self.seating_option.set = ("Select Seating")
        self.option_menu = ttk.OptionMenu(self.details_frame, self.seating_field, "Lower Hall", "Upper Gallery", "VIP")
        
        # Lay out the entry fields in a grid
        self.first_name_label.grid(row=0, column=0, sticky="W")
        self.first_name_field.grid(row=0, column=1)
        self.surname_label.grid(row=1, column=0, sticky="W")
        self.surname_field.grid(row=1, column=1)
        self.seating_option.grid(row=2, column=0, sticky="W")
        self.option_menu.grid(row=2, column=1)
        
        def confirm():
            print("First Name:", self.first_name_field.get())
            print("Surname:", self.surname_field.get())
            print("Seating Area:", self.seating_field.get())
        
        confirm_button = ttk.Button(self.details_frame, text="Confirm", command=confirm)
        confirm_button.grid(row=3, column=1, sticky="E")

class filmImg(ttk.Frame):
    
    # --- Film Image ---
        # In a seperate frame you will have the movie poster with a book now button underneath
    def __init__(self, parent, *args, **kwargs):
        self.film = kwargs.pop("film")
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)
        
        # --- Film Information ---
        # In this frame it will contain each film listing such as; Title and Year, Genre and cast & bio of movie.
        self.inspect_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=1000, height=1000)
        self.inspect_title = ttk.Label(self.inspect_frame,text ="Title:")
        self.inspect_year = ttk.Label(self.inspect_frame,text ="Year:")
        self.inspect_rating = ttk.Label(self.inspect_frame,text ="Rating:")
        self.inspect_age_rating = ttk.Label(self.inspect_frame,text ="Age Rating:")
        self.inspect_synopsis = ttk.Label(self.inspect_frame, text ="Synopsis:")
        self.inspect_duration = ttk.Label(self.inspect_frame,text ="Duration:")
        self.inspect_cast = ttk.Label(self.inspect_frame,text ="Cast:")
        self.inspect_genres = ttk.Label(self.inspect_frame,text ="Genres:")
        
        #BACKUP LABEL IF NO FILMS THAT DAY

        # --- Select Show Time
        selected_value = tk.StringVar()
        self.morning_film = ttk.Radiobutton(self.inspect_frame, text="Morning", value="option 1", variable="morning")
        self.afternoon_film = ttk.Radiobutton(self.inspect_frame, text="Afternoon", value="option 2", variable="afternoon")
        self.evening_film = ttk.Radiobutton(self.inspect_frame, text="Evening", value="option 3", variable="evening")
        
        #Poster for Film next to information on that film
        self.poster_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=200, height=200)
        self.film_Image = ImageTk.PhotoImage(Image.open(self.film.poster).resize((200, 200)))
        self.img_label = ttk.Label(self.poster_frame, image=self.film_Image)

        # --- Gridding ---
        self.inspect_frame.grid(column=0, row=0, rowspan=3, sticky="nsew")
        self.inspect_title.grid(column=0, row=0)
        self.inspect_year.grid(column=0, row=1)
        self.inspect_rating.grid(column=0, row=2)
        self.inspect_age_rating.grid(column=1, row=1)
        self.inspect_synopsis.grid(column=0, row=3)
        self.inspect_duration.grid(column=1, row=0)
        self.inspect_cast.grid(column=1, row=2)
        self.inspect_genres.grid(column=1, row=2)

        self.morning_film.grid(column=0, row=3)
        self.afternoon_film.grid(column=1, row=3)
        self.evening_film.grid(column=2, row=3)

        self.poster_frame.grid(column=1, row=0, rowspan=2, sticky="nsew")
        self.img_label.grid(column=2, row=0)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # --- BOOK BUTTON ---
        self.book_button = ttk.Button(self.inspect_frame, text="Book Now", command=self.book)
        self.book_button.grid(column=3, row=5, rowspan=1)

    def book(self):
        details_window = tk.Toplevel()
        enter_details = enterDetails(self, details_window)
        enter_details.pack(side="top", fill="both", expand=True)


class NewBooking(ttk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        for i in range(24):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(3, weight=1)

        today = datetime.now()
        day_beginning = datetime.combine(today, time(hour=0, minute=0))
        day_end = datetime.combine(today, time(hour=23, minute=59))

        today_films = session.query(Film).join(Film.showings).join(Showing.screen).filter(
            Screen.cinema_id == parent.current_user.cinema_id,
            Showing.show_time >= day_beginning,
            Showing.show_time <= day_end
            )

        film_tiles = []

        for i, film in enumerate(today_films):
            film_tiles.append(filmImg(self, film=film).grid(column=3, row=i, rowspan=3, sticky="nsew"))
