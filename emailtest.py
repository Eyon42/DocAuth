import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.message import EmailMessage

smtpServer = "smtp.gmail.com"
port = 587

load_dotenv()
myEmail = os.environ.get("VERIFICATION_EMAIL_ADDR")
password = os.environ.get("VERIFICATION_EMAIL_PASS")

context = ssl.create_default_context()




server = smtplib.SMTP(smtpServer,port)
server.starttls(context=context)
server.login(myEmail, password)

# newEmail = """
# Hello Email World! :)
# """
# server.sendmail(myEmail, "butcheringdeutsch@gmail.com", newEmail)

recievers = ["butcheringdeutsch@gmail.com"]

m = EmailMessage()
m.set_content("Hello World!")
m["Subject"] = "Trying out emails on python"
m["From"] = myEmail
m["To"] = recievers

server.send_message(m)


server.quit()
