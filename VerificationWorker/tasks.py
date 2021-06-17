from .celery import app

from .db import models, db_session


# Here are defined the tasks

@app.task
@db_session
def get_first_user(session):
    return session.query(models.User).first().name
