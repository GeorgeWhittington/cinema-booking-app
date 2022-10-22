from sqlalchemy import Column, Table, ForeignKey

from database_models import Base

film_genre = Table(
    "film_genre",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True)
)
