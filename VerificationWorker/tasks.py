from .celery import app
from .db import models, db_session
from .emails import send_mail

# Here are defined the tasks

@app.task
@db_session
def get_first_user(session):
    return session.query(models.User).first().name


@app.task
def send_verification_email(mail, verification_code):

    # To Do:
    # generate_verification_link()
    # this takes the email and username and combines them with the secret key
        # Verification link
        # An api endpoint with a query argument for verification key
        # The enpoint validates the key and changes the validation status

    link_to_end_point = "" #TO-Do
    verification_link = f"{link_to_end_point}/?verification_code={verification_code}"
    content = f"""
    <a href={verification_link}>click this link<\a> [WIP]"
    Or POST this to "{link_to_end_point}"
    {{
        verification_code: {verification_code}
    }}
    """
    send_mail(mail, "Doc Auth Account Verification", content, sender="VERIFICATION")