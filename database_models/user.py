import enum

import bcrypt
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from database_models import Base


class Authority(enum.Enum):
    BOOKING = "booking"
    ADMIN = "admin"
    MANAGER = "manager"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey("cinema.id"))
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    authority = Column(Enum(Authority), nullable=False)

    cinema = relationship("Cinema", back_populates="users")
    bookings = relationship("Booking", back_populates="employee")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, authority={self.authority}, cinema={self.cinema})>"

    def verify_password(self, password):
            return bcrypt.checkpw(password.encode("utf-8"), self.password)

    @staticmethod
    def hash_password(password):
        if len(password) > 72:
            raise ValueError("Password is longer than 72 characters and cannot be accepted by bcrypt.")

        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
