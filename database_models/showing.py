from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from database_models import Base


class Showing(Base):
    """A showing of a film. Number of booked seats can be tracked by
    querying the related bookings."""
    __tablename__ = "showings"

    id = Column(Integer, primary_key=True)
    screen_id = Column(Integer, ForeignKey("screens.id"))
    film_id = Column(Integer, ForeignKey("films.id"))
    # Only recording start time since I'm assuming that pricing is based on that? 
    # Clarify with Zaheer what happens when film is shown across two pricing time ranges
    # e.g. starts at 11:00 at morning price, finishes at 13:10 with afternoon price
    show_time = Column(DateTime, nullable=False)

    screen = relationship("Screen", back_populates="showings")
    film = relationship("Film", back_populates="showings")
    bookings = relationship("Booking", back_populates="showing")

    def __repr__(self):
        return f"<Showing(id={self.id}, screen={self.screen}, film={self.film}, show_time={self.show_time})>"