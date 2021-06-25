from .celery import app
from .db import models, db_session
from .emails import send_mail

# Here are defined the tasks

@app.task
@db_session
def get_first_user(session):
    return session.query(models.User).first().name


@app.task
@db_session
def send_verification_email(session, username, mail):

    # To Do:
    # generate_verification_link()
    # this takes the email and username and combines them with the secret key
        # Verification link
        # An api endpoint with a query argument for verification key
        # The enpoint validates the key and changes the validation status

    verification_link = generate_verification_link(username, mail)
    content = f"Verification code: {verification_link}"
    send_mail(mail, "Doc Auth Account Verification", content, sender="ADMIN")