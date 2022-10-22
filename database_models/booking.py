from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database_models import Base


class Booking(Base):
    """A booking to see a showing of a film.
    
    Card details are not stored in database, they are "sent" to 
    payment handler securely.
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    showing_id = Column(Integer, ForeignKey("showings.id"))
    lower_booked = Column(Integer, nullable=False)
    upper_booked = Column(Integer, nullable=False)
    vip_booked = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    showing = relationship("Showing", back_populates="bookings")

    def __repr__(self):
        return f"<Booking(id={self.id}, showing={self.showing})>"