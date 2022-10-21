from contextlib import contextmanager

from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from database_models.user import User

from config import DATABASE_URI

if DATABASE_URI:
    # You can define the database uri in the config/config.json file. 
    # It needs to be in the format explained here: https://docs.sqlalchemy.org/en/14/core/engines.html#sqlite
    engine = create_engine(DATABASE_URI)
else:
    # if no database is specified, use in-memory testing db
    engine = create_engine("sqlite://")

session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)

# Issues all CREATE TABLE commands to database connected to in create_engine
# If a table already exists in that database, this does not try to override it. 
# You will need to manually issue ALTER TABLE sql to the database, or delete it and start over
Base.metadata.create_all(engine)

@contextmanager
def session_scope():
    """Allows you to use the SQLAlchemy session using a context manager.
    
    When you use this method to create a session to access the database it will always
    commit the session for you at the end. If any errors occur during the session it will 
    ensure the session still gets closed."""
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        session.close()
