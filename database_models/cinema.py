from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database_models import Base


class Cinema(Base):
    """A cinema.
    
    The prices at a cinema are determined by the city they are in.
    """
    __tablename__ = "cinemas"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    name = Column(String, nullable=False, unique=True)

    city = relationship("City", back_populates="cinemas")
    screens = relationship("Screen", back_populates="cinema")
    users = relationship("User", back_populates="cinema")

    def __repr__(self):
        return f"<Cinema(id={self.id}, name={self.name}, city={self.city})>"