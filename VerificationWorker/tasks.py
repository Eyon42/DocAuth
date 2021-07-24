from .celery import app
#from .db import models, db_session
from .emails import send_mail

# Here are defined the tasks

# It seems I'm getting some probems with circular imports when using the db.
# For now I won't use it here until I decide how to implement it without
# copying and pasting files.

# @app.task
# @db_session
# def get_first_user(session):
#     return session.query(models.User).first().name


@app.task
def send_verification_email(mail, verification_code, link_to_end_point):

    # To Do:
    # generate_verification_link()
    # this takes the email and username and combines them with the secret key
        # Verification link
        # An api endpoint with a query argument for verification key
        # The enpoint validates the key and changes the validation status

    verification_link = f"{link_to_end_point}/?verification_code={verification_code}"
    content = {
        "text" : 
        """
        POST this to "{link_to_end_point}" with your auth token.
        {{
            verification_code: {verification_code}
        }}
        """,
        "html" : 
    f"""
    <p>
    Note: The following link should be replaced by somehting in the frontend which handles auth.
    <br>
    For now use the post method with credentials
    <br>
    <a href="{verification_link}">click this link</a>
    <br>
    Or POST this to "{link_to_end_point}"
    <br>
    <pre><code>
    {{
        "verification_code" : "{verification_code}"
    }}
    </code></pre>
    </p>
    """
    }
    send_mail(mail, "Doc Auth Account Verification", content, sender="VERIFICATION")