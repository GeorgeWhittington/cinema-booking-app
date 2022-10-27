from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database_models import Base
from database_models.m2m_tables import film_genre


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    films = relationship("Film", secondary=film_genre, back_populates="genres")

    def __repr__(self):
        return f"<Genre(id={self.id}, name={self.name})>"