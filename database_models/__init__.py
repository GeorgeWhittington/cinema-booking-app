from contextlib import contextmanager

from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from database_models.user import User

from config import DATABASE_URI

if DATABASE_URI:
    engine = create_engine(DATABASE_URI)
else:
    # if no database is specified, use in-memory testing db
    engine = create_engine("sqlite://")

session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)

Base.metadata.create_all(engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        session.close()
