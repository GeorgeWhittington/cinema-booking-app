from database_models import session_scope, User, Cinema, City, Authority

if __name__ == "__main__":
    with session_scope() as session:
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
        for row in list(cities.values()) + cinemas + users:
            session.add(row)