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
    def __init__(self, parent, *args, **kwargs):
        self.dismiss = kwargs.pop("dismiss")
        self.film = kwargs.pop("film")
        self.time_period = kwargs.pop("time_period")

        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        now = datetime.now()

        if self.time_period == "morning":
            time_beginning = datetime.combine(now, time(hour=8, minute=0))
            time_end = datetime.combine(now, time(hour=11, minute=59))
        elif self.time_period == "afternoon":
            time_beginning = datetime.combine(now, time(hour=12, minute=0))
            time_end = datetime.combine(now, time(hour=16, minute=59))
        elif self.time_period == "evening":
            time_beginning = datetime.combine(now, time(hour=17, minute=0))
            time_end = datetime.combine(now, time(hour=23, minute=59))

        self.showings = session.query(Showing).filter(
            Showing.film_id == self.film.id,
            Showing.show_time >= time_beginning,
            Showing.show_time <= time_end
        ).all()

        self.showings_formatted = []
        for showing in self.showings:
            self.showings_formatted.append(f"{showing.film.title}, {showing.show_time}")

        #To enter details for booking
        self.details_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=1000, height=1000)
        self.details_title = ttk.LabelFrame(self.details_frame, text="Booking Details")
        self.showing_label = ttk.Label(self.details_frame, text="Film Showing:")
        self.showing_entry = ttk.Combobox(self.details_frame)
        self.showing_entry["values"] = self.showings_formatted

        self.full_name_label = ttk.Label(self.details_frame, text="Full Name:")
        self.full_name_field = ttk.Entry(self.details_frame)
        self.phone_no_label = ttk.Label(self.details_frame, text="Phone Number:")
        self.phone_no_field = ttk.Entry(self.details_frame)
        self.Email_label = ttk.Label(self.details_frame, text="E-Mail:")
        self.Email_field = ttk.Entry(self.details_frame)

        self.seating_label = ttk.Label(self.details_frame, text="Seating Area:")

        self.seating_frame = ttk.Frame(self.details_frame)
        self.seating_option_lh = ttk.Label(self.seating_frame, text="Lower Hall")
        self.seating_no_value_lh = ttk.Spinbox(self.seating_frame, from_=0.0, to=10.0)
        self.seating_option_ug = ttk.Label(self.seating_frame, text="Upper Gallery")
        self.seating_no_value_ug = ttk.Spinbox(self.seating_frame, from_=0.0, to=10.0)
        self.seating_option_vip = ttk.Label(self.seating_frame, text="VIP")
        self.seating_no_value_vip = ttk.Spinbox(self.seating_frame, from_=0.0, to=10.0)

        
        widgets = [
            (self.showing_label , self.showing_entry),
            (self.full_name_label , self.full_name_field),
            (self.phone_no_label , self.phone_no_field),
            (self.Email_label , self.Email_field),
            (self.seating_label , self.seating_frame)
        ]

        for y, (label, field) in enumerate(widgets):
            label.grid(column=0, row=y, sticky="w")
            field.grid(column=1, row=y, sticky="ew")
        
        self.details_frame.grid(column=0, row=0)

        self.details_frame.columnconfigure(0, weight=0)
        self.details_frame.columnconfigure(1, weight=1)

        self.seating_option_lh.grid(column=0, row=0)
        self.seating_no_value_lh.grid(column=1, row=0)
        self.seating_option_ug.grid(column=2, row=0)
        self.seating_no_value_ug.grid(column=3, row=0)
        self.seating_option_vip.grid(column=4, row=0)
        self.seating_no_value_vip.grid(column=5, row=0)

        #Total cost real time
        self.price_frame = ttk.Frame(self)
        self.total_price = 0
        self.total_price_label = ttk.Label(self.price_frame, text="Total Cost:")
        self.total_price_field = ttk.Label(self.price_frame, text="£0.00")

    def update_total_price(self, price):
        selected_showing = self.showing_entry.get()
        film_title, show_time = selected_showing.split(", ")
        film = session.query(Film).filter(Film.title == film_title).one()

        price = film.price

        self.total_price += price
        self.total_price_field.config(text=str(self.total_price))


    def add_details(self):
        self.showing_entry.bind("<<ComboboxSelected", self.update_total_price)
        
        self.button_frame = ttk.Frame(self)
        self.confirm_button = ttk.Button(self.button_frame, text="Confirm", command=self.confirm)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.dismiss)
        
        self.price_frame.grid(column=0, row=0)
        self.button_frame.grid(column=0, row=2)
        self.confirm_button.grid(column=0, row=1)
        self.cancel_button.grid(column=1, row=1)
    
    def confirm(self):
        pass

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
        # get showing time period
        self.master.master.show_modal(enterDetails, {
            "film": self.film,
            "time_period": "morning"
        })


class NewBooking(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        self.cinema_location = ttk.Label(self, text=f"You are booking at: {self.master.current_user.cinema.name}")
        self.cinema_location.grid(column=0, row=0, sticky="ne")

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

        if len(self.todays_films) == 0:
            self.no_films_label = ttk.Label(self, text="There are no films showing today at your cinema.")
            self.no_films_label.grid(column=0, row=1)

            self.next_button.destroy()
            self.prev_button.destroy()
            return

        self.page = self.get_page()

        self.film_tiles = []
        self.display_films()

    def display_films(self):
        for tile in self.film_tiles:
            tile.grid_remove()
            tile.destroy()

        self.film_tiles = []

        for i, film in enumerate(self.page):
            film_img = filmImg(self, film=film)
            film_img.grid(column=0, row=i+1, sticky="nsew")
            self.film_tiles.append(film_img)

        self.button_frame.grid(column=0, row=len(self.page.items)+1)

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