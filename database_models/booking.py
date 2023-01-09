from datetime import time

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database_models import Base


class Booking(Base):
    """A booking to see a showing of a film.

    Card details are not stored in database, they are "sent" to
    payment handler securely.
    """
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True)
    showing_id = Column(Integer, ForeignKey("showing.id"))
    employee_id = Column(Integer, ForeignKey("user.id"))
    lower_booked = Column(Integer, nullable=False)
    upper_booked = Column(Integer, nullable=False)
    vip_booked = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    showing = relationship("Showing", back_populates="bookings")
    employee = relationship("User", back_populates="bookings")  # Employee that booked these tickets

    def __repr__(self):
        return f"<Booking(id={self.id}, showing={self.showing})>"

    def calculate_price(self):
        return self.calculate_booking_price(self.showing, self.lower_booked, self.upper_booked, self.vip_booked)

    @staticmethod
    def calculate_booking_price(showing, lower_booked, upper_booked, vip_booked):
        city = showing.screen.cinema.city

        show_time = time(
            hour=showing.show_time.hour,
            minute=showing.show_time.minute)

        if time(8, 0, 0) <= show_time < time(12, 0, 0):
            # Starts between 8am-11:59am
            base_price = city.morning_price
        elif time(12, 0, 0) <= show_time < time(17, 0, 0):
            # Starts between 12pm-4:59pm
            base_price = city.afternoon_price
        elif time(17, 0, 0) <= show_time <= time(23, 59, 59):
            # Starts between 5pm-12am
            base_price = city.evening_price

        price = base_price * lower_booked
        price += base_price * upper_booked * 1.2
        price += (base_price * vip_booked * 1.2) * 1.2

        return round(price, 2)