from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from database_models import Base


class Showing(Base):
    """A showing of a film. Number of booked seats can be tracked by
    querying the related bookings."""
    __tablename__ = "showing"

    id = Column(Integer, primary_key=True)
    screen_id = Column(Integer, ForeignKey("screen.id"))
    film_id = Column(Integer, ForeignKey("film.id"))
    # Only recording start time since pricing is based on that 
    # e.g. starts at 11:00 at morning price, even though it ends in afternoon range
    show_time = Column(DateTime, nullable=False)

    screen = relationship("Screen", back_populates="showings")
    film = relationship("Film", back_populates="showings")
    bookings = relationship("Booking", back_populates="showing")

    def __repr__(self):
        return f"<Showing(id={self.id}, screen={self.screen}, film={self.film}, show_time={self.show_time})>"