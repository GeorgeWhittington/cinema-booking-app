from enum import Enum
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
from sqlalchemy import Column, Float, Integer, Interval, String, Text

from sqlalchemy.sql import and_
from datetime import datetime, time
from misc.constants import ADD, EDIT, FILM_FORMAT, MIDNIGHT, EIGHT_AM
from paginate import Page

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
        self.wrapper_frame = ttk.Frame(self, borderwidth=5,relief="ridge")
        self.title_frame = ttk.Frame(self.wrapper_frame, borderwidth=5)
        self.inspect_frame = ttk.Frame(self.wrapper_frame, borderwidth=5)
        self.rating_frame = ttk.Frame(self.wrapper_frame, borderwidth=5)
        self.booking_frame = ttk.Frame(self.wrapper_frame)

        self.title = ttk.Label(self.title_frame,text = self.film.title)
        self.year = ttk.Label(self.title_frame,text = self.film.year_published)
        self.duration = ttk.Label(self.title_frame,text = self.film.string_conv("duration"))
        
        self.synopsis = ttk.Label(self.inspect_frame, text = self.film.synopsis, wraplength=800)
        self.cast = ttk.Label(self.inspect_frame,text = self.film.cast)

        self.rating = ttk.Label(self.rating_frame,text = self.film.string_conv("rating"))
        self.age_rating = ttk.Label(self.rating_frame,text = self.film.age_rating.value)
        self.genres = ttk.Label(self.rating_frame,text = self.film.string_conv("genres"))
        # --- BOOK BUTTON ---
        self.book_button = ttk.Button(self.booking_frame, text="Book Now", command=self.book)
        
        #BACKUP LABEL IF NO FILMS THAT DAY

        # --- Select Show Time
        morning_film = tk.StringVar()
        afternoon_film = tk.StringVar()
        evening_film = tk.StringVar()
        
        self.morning_film = ttk.Radiobutton(self.booking_frame, text="Morning", value="option 1", variable= morning_film)
        self.afternoon_film = ttk.Radiobutton(self.booking_frame, text="Afternoon", value="option 2", variable= afternoon_film)
        self.evening_film = ttk.Radiobutton(self.booking_frame, text="Evening", value="option 3", variable= evening_film)
        
        #Poster for Film next to information on that film
        film_img = self.film.poster if self.film.poster else "assets/placeholder.png"
        self.poster_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=200, height=200)
        self.film_Image = ImageTk.PhotoImage(Image.open(film_img).resize((200, 200)))
        self.img_label = ttk.Label(self.poster_frame, image=self.film_Image)

        # --- Gridding ---
        self.wrapper_frame.grid(column=0, row=0, sticky="nsew")
        self.title_frame.grid(column=0, row=0, sticky="nsew")
        self.inspect_frame.grid(column=0, row=1, sticky="nsew")
        self.rating_frame.grid(column=0, row=2, sticky="nsew")
        self.booking_frame.grid(column=0, row=3, sticky="nsew")
        self.poster_frame.grid(column=1, row=0, sticky="nsew")

        self.title.grid(column=0, row=0)
        self.year.grid(column=1, row=0)
        self.duration.grid(column=2, row=0)
        
        self.synopsis.grid(column=0, row=0, sticky="w")
        self.cast.grid(column=0, row=1, sticky="w")

        self.age_rating.grid(column=0, row=0)
        self.genres.grid(column=1, row=0)
        self.rating.grid(column=2, row=0)

        self.morning_film.grid(column=0, row=0, sticky="w")
        self.afternoon_film.grid(column=1, row=0, sticky="w")
        self.evening_film.grid(column=2, row=0, sticky="w")
        self.book_button.grid(column=3, row=0, sticky="e")

        self.img_label.grid(column=0, row=0)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

    def book(self):
        details_window = tk.Toplevel()
        enter_details = enterDetails(self, details_window)
        enter_details.pack(side="top", fill="both", expand=True)


class NewBooking(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        self.button_frame = ttk.Frame(self)
        self.prev_button = ttk.Button(self.button_frame, text="Previous Page", command=self.prev_page)
        self.next_button = ttk.Button(self.button_frame, text="Next Page", command=self.next_page)

        self.prev_button.grid(column=0, row=0)
        self.next_button.grid(column=1, row=0)

        today = datetime.now()
        day_beginning = datetime.combine(today, time(hour=0, minute=0))
        day_end = datetime.combine(today, time(hour=23, minute=59))

        self.todays_films = session.query(Film).join(Film.showings).join(Showing.screen).filter(
            Screen.cinema_id == parent.current_user.cinema_id,
            Showing.show_time >= day_beginning,
            Showing.show_time <= day_end
        ).all()

        self.page = self.get_page()

        self.film_tiles = []
        self.display_films()

    def display_films(self):
        for tile in self.film_tiles:
            tile.grid_remove()
            tile.destroy()

        self.film_tiles = []

        print(self.page.items)

        for i, film in enumerate(self.page):
            film_img = filmImg(self, film=film)
            film_img.grid(column=0, row=i, sticky="nsew")
            self.film_tiles.append(film_img)

        self.button_frame.grid(column=0, row=len(self.page.items))

    def prev_page(self):
        if self.page.page == 1:
            return

        self.page = self.get_page(page=self.page.page - 1)
        self.display_films()

    def next_page(self):
        page = self.get_page(page=self.page.page + 1)
        if not page.items:
            return

        self.page = page
        self.display_films()

    def get_page(self, page=1):
        return Page(self.todays_films, page=page, items_per_page=4)