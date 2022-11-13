from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from database_models import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    morning_price = Column(Float, nullable=False)
    afternoon_price = Column(Float, nullable=False)
    evening_price = Column(Float, nullable=False)

    cinemas = relationship("Cinema", back_populates="city")

    def __repr__(self):
        return f"<City(id={self.id}, name={self.name}, morning_price={self.morning_price}, afternoon_price={self.afternoon_price}, evening_price={self.evening_price})>"