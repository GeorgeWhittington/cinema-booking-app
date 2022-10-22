from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database_models import Base


class Screen(Base):
    __tablename__ = "screens"

    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey("cinemas.id"))
    lower_capacity = Column(Integer, nullable=False)
    upper_capacity = Column(Integer, nullable=False)
    vip_capacity = Column(Integer, nullable=False)

    cinema = relationship("Cinema", back_populates="screens")
    showings = relationship("Showing", back_populates="screen")

    def __repr__(self):
        return f"<Screen(id={self.id}, cinema={self.cinema})>"