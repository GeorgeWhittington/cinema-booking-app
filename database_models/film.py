import enum

from sqlalchemy import Column, ForeignKey, Table, Integer, String, Float, Enum, Interval, Text
from sqlalchemy.orm import relationship

from database_models import Base
from database_models.m2m_tables import film_genre
from misc.utils import get_hours_minutes


class AgeRatings(enum.Enum):
    U = "U"
    PG = "PG"
    TWELVE = "12"
    FIFTEEN = "15"
    EIGHTEEN = "18"


class Film(Base):
    __tablename__ = "film"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # Don't enforce unique, films can have same name
    year_published = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    age_rating = Column(Enum(AgeRatings), nullable=False)
    duration = Column(Interval, nullable=False)  # Translates to datetime.timedelta object
    synopsis = Column(Text, nullable=False)
    cast = Column(String, nullable=False)
    poster = Column(String, nullable=True)

    genres = relationship("Genre", secondary=film_genre, back_populates="films")
    showings = relationship("Showing", back_populates="film")

    def __repr__(self):
        return f"<Film(id={self.id}, title={self.title}, year_published={self.year_published})>"

    def string_conv(self, attr):
        """When provided with the attribute of a film, converts it to its string formatted form."""
        if attr == "rating":
            return f"{int(self.rating * 100)}/100"
        if attr == "duration":
            h, m = get_hours_minutes(self.duration.total_seconds())
            return f"{h}h {m}m"
        if attr == "genres":
            return ", ".join(genre.name for genre in self.genres)

        return str(getattr(self, attr))