import bcrypt
from sqlalchemy import Column, Integer, String

from database_models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
    
    @staticmethod
    def hash_password(password):
        if len(password) > 72:
            raise ValueError("Password is longer than 72 characters and cannot be accepted by bcrypt.")

        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

_old_init = User.__init__

def _new_init(self, password, **kwargs):
    kwargs["password"] = User.hash_password(password)
    _old_init(self, **kwargs)

User.__init__ = _new_init
