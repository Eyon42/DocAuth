import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
PORT = 587

load_dotenv()

def send_mail(recievers, subject, content, sender="ADMIN"):

    email = os.environ.get(sender + "_EMAIL_ADDR")
    password = os.environ.get(sender + "_EMAIL_PASS")
    
    # Connects to server
    context = ssl.create_default_context()
    server = smtplib.SMTP(SMTP_SERVER,PORT)
    server.starttls(context=context)
    server.login(email, password)

    # Assemble message
    m = EmailMessage()
    m.set_content(content)
    m["Subject"] = subject
    m["From"] = email
    m["To"] = recievers

    server.send_message(m)
    server.quit()
