from sqlalchemy import Column, Table, ForeignKey

from database_models import Base

film_genre = Table(
    "film_genre",
    Base.metadata,
    Column("film_id", ForeignKey("film.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True)
)
