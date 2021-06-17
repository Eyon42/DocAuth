from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from DocAuth.api import models
from DocAuth.settings import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True, future=True)

def get_session():
    return Session(engine)

def db_session(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        with get_session() as session:
            return f(*args, **kwargs, session=session)
    return wrapped
