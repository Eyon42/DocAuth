import smtplib
import ssl
import os
from dotenv import load_dotenv
#from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    m = MIMEMultipart('alternative')
    m["Subject"] = subject
    m["From"] = email
    m["To"] = recievers

    part1 = MIMEText(content["text"], 'plain')
    part2 = MIMEText(content["html"], 'html')
    m.attach(part1)
    m.attach(part2)

    server.send_message(m)
    server.quit()
