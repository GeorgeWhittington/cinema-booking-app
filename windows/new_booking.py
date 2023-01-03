from tkinter import ttk
from PIL import ImageTk, Image
from database_models import session, Showing, Cinema, Film, Screen, Genre, AgeRatings
from windows import FilmShowingWindow, FilmWindow

class filmImg(ttk.Frame):

    # --- Film Image ---
        # In a seperate frame you will have the movie poster with a book now button underneath
    def __init__(self, filepath, parent, *args, **kwargs):
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
        
        #Poster for Film next to information on that film
        self.poster_frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=200, height=200)
        self.film_Image = ImageTk.PhotoImage(Image.open(filepath).resize((200, 200)))
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

        self.poster_frame.grid(column=1, row=0, rowspan=2, sticky="nsew")
        self.img_label.grid(column=2, row=0)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        # --- BOOK BUTTON ---
        self.book_button = ttk.Button(self.inspect_frame, text="book now",)
        self.book_button.grid(column=3, row=5, rowspan=1)


class NewBooking(ttk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        kwargs["padding"] = (3, 3, 3, 3)
        super().__init__(parent, *args, **kwargs)

        for i in range(24):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(3, weight=1)
    
        filmImg("./assets/american_history_x.jpeg", self, *args, **kwargs).grid(column=3, row=0, rowspan=3, sticky="nsew")
        filmImg("./assets/dkr.jpg", self, *args, **kwargs).grid(column=3, row=4, rowspan=3, sticky="nsew")
        filmImg("./assets/lifeofb.jpg", self, *args, **kwargs).grid(column=3, row=8, rowspan=3, sticky="nsew")
        filmImg("./assets/spirited_away.jpg", self, *args, **kwargs).grid(column=3, row=12, rowspan=3, sticky="nsew")
        filmImg("./assets/up.jpg", self, *args, **kwargs).grid(column=3, row=16, rowspan=3, sticky="nsew")


# --- Booking Button ---
        # Underneath each film will be a "Book Now" button for easy booking
            # --- INSERT LINK TO SHOW VIEWINGS PAGE ---
    #def book_button(self):
            #takes to film_showing.py
        # Callback for view showings button.
        #try:
            #selected_id = int(self.treeview.selection()[0])
        #except IndexError:
            #self.master.switch_window(FilmShowingWindow)
            #return

        #film = session.query(Film).get(selected_id)
        #if not film:
            #return

        #self.master.switch_window(FilmShowingWindow, kwargs={"film_filter": film.id})