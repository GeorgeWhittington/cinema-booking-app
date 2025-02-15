from datetime import datetime, timedelta

from database_models import session, User, Cinema, City, Authority, Screen, Film, AgeRatings, Genre, Showing, Booking

if __name__ == "__main__":
    cities = {
        "birmingham": City(name="Birmingham", morning_price=5.0, afternoon_price=6.0, evening_price=7.0),
        "bristol": City(name="Bristol", morning_price=6.0, afternoon_price=7.0, evening_price=8.0),
        "cardiff": City(name="Cardiff", morning_price=5.0, afternoon_price=6.0, evening_price=7.0),
        "london": City(name="London", morning_price=10.0, afternoon_price=11.0, evening_price=12.0)
    }
    cinemas = [
        Cinema(name="Birmingham Broadway Plaza", city=cities["birmingham"]),
        Cinema(name="Birmingham New Street", city=cities["birmingham"]),
        Cinema(name="Bristol Union Street", city=cities["bristol"]),
        Cinema(name="Cardiff Hemingway Road", city=cities["cardiff"]),
        Cinema(name="London Covent Garden", city=cities["london"]),
        Cinema(name="London Haymarket", city=cities["london"]),
        Cinema(name="London Leicester Square", city=cities["london"])
    ]
    users = [
        User(username="user", password=User.hash_password("pass"), cinema=cinemas[2], authority=Authority.BOOKING),
        User(username="admin", password=User.hash_password("pass1"), cinema=cinemas[2], authority=Authority.ADMIN),
        User(username="manager", password=User.hash_password("pass2"), cinema=cinemas[2], authority=Authority.MANAGER)
    ]
    screens = [
        Screen(name="Screen One", cinema=cinemas[2], lower_capacity=60, upper_capacity=130, vip_capacity=10),
        Screen(name="Screen Two", cinema=cinemas[2], lower_capacity=60, upper_capacity=130, vip_capacity=10),
        Screen(name="Screen One", cinema=cinemas[3], lower_capacity=60, upper_capacity=130, vip_capacity=10),
        Screen(name="Screen Two", cinema=cinemas[3], lower_capacity=60, upper_capacity=130, vip_capacity=10)
    ]
    genres = [
        Genre(name="Comedy"),
        Genre(name="Satire"),
        Genre(name="Action"),
        Genre(name="Thriller"),
        Genre(name="Drama"),
        Genre(name="Crime"),
        Genre(name="Adventure"),
        Genre(name="Family"),
        Genre(name="Fantasy"),
    ]
    films = [
        Film(
            title="Life of Brian", year_published=1979, rating=0.8,
            age_rating=AgeRatings.FIFTEEN, duration=timedelta(hours=1, minutes=34),
            synopsis="A young man, Brian, who was born one stable down and on the same night as Jesus, becomes intrigued by a young rebel, Judith. To try and impress her, Brian joins the independence movement against the Romans, the People's Front of Judea. However, in an attempt to hide from the Romans, he relays some of the teachings he heard from Jesus, which ends up spurring a crowd to believe he is the Messiah. While trying to get rid of his followers and reunite with Judith, he embarks on several misadventures.",
            cast="Graham Chapman, John Cleese, Michael Palin", genres=[genres[0], genres[1]], poster="assets/lifeofb.jpg"),
        Film(
            title="The Dark Knight Rises", year_published=2012, rating=0.8,
            age_rating=AgeRatings.TWELVE, duration=timedelta(hours=2, minutes=44),
            synopsis="Eight years after the Joker's reign of anarchy, Batman, with the help of the enigmatic Selina Kyle, is forced from his exile to save Gotham City from the brutal guerrilla terrorist Bane.",
            cast="Christian Bale, Tom Hardy, Anne Hathaway", genres=[genres[2], genres[3]], poster="assets/dkr.jpg"),
        Film(
            title="American History X", year_published=1998, rating=0.9,
            age_rating=AgeRatings.EIGHTEEN, duration=timedelta(hours=1, minutes=59),
            synopsis="A former neo-nazi skinhead tries to prevent his younger brother from going down the same wrong path that he did.",
            cast="Edward Norton, Edward Furlong, Beverly D'Angleo, Jennifer Lien", genres=[genres[4], genres[5]], poster="assets/american_history_x.jpeg"),
        Film(
            title="UP", year_published=2009, rating=0.8,
            age_rating=AgeRatings.U, duration=timedelta(hours=1, minutes=36),
            synopsis="78-year-old Carl Fredricksen travels to Paradise Falls in his house equipped with balloons, inadvertently taking a young stowaway.",
            cast="Edward Asner, Jordan Nagai", genres=[genres[6], genres[7]], poster="assets/up.jpg"),
        Film(
            title="Spirited Away", year_published=2001, rating=0.9,
            age_rating=AgeRatings.PG, duration=timedelta(hours=2, minutes=5),
            synopsis="During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.",
            cast="Daveigh Chase, Suzanne Pleshette", genres=[genres[8], genres[6]], poster="assets/spirited_away.jpg")
    ]
    showings = [
        Showing(screen=screens[0], film=films[0], show_time=datetime(year=2022, month=10, day=20, hour=11)),
        Showing(screen=screens[1], film=films[0], show_time=datetime(year=2022, month=11, day=20, hour=14)),
        Showing(screen=screens[1], film=films[0], show_time=datetime(year=2022, month=11, day=20, hour=18)),
        Showing(screen=screens[2], film=films[2], show_time=datetime(year=2022, month=11, day=20, hour=10)),
        Showing(screen=screens[2], film=films[3], show_time=datetime(year=2022, month=11, day=20, hour=12)),
        Showing(screen=screens[2], film=films[4], show_time=datetime(year=2022, month=11, day=20, hour=17))
    ]
    bookings = [
        Booking(
            showing=showings[0], employee=users[0], lower_booked=0, upper_booked=1, vip_booked=0,
            name="Sally", phone="7348265873", email="sally@gmail.com"),
        Booking(
            showing=showings[0], employee=users[0], lower_booked=1, upper_booked=2, vip_booked=0,
            name="James", phone="7348265873", email="james@gmail.com"),
        Booking(
            showing=showings[0], employee=users[1], lower_booked=3, upper_booked=0, vip_booked=0,
            name="Nora", phone="7348265873", email="nora@gmail.com"),
        Booking(
            showing=showings[5], employee=users[1], lower_booked=0, upper_booked=0, vip_booked=3,
            name="Mo", phone="7348265873", email="mohammed@gmail.com"),
        Booking(
            showing=showings[5], employee=users[0], lower_booked=1, upper_booked=2, vip_booked=0,
            name="Sally", phone="7348265873", email="sally@gmail.com"),
        Booking(
            showing=showings[5], employee=users[0], lower_booked=0, upper_booked=0, vip_booked=4,
            name="Sally", phone="7348265873", email="sally@gmail.com"),
        Booking(
            showing=showings[5], employee=users[2], lower_booked=0, upper_booked=1, vip_booked=1,
            name="Sally", phone="7348265873", email="sally@gmail.com"),
    ]

    for row in list(cities.values()) + cinemas + users + screens + films + genres + showings:
        session.add(row)

    session.commit()