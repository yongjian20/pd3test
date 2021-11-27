import sendgrid
import os
from sendgrid.helpers.mail import *
from dotenv import load_dotenv

load_dotenv()

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))


def send_email(recipient, subject, message):
    content = Content("text/plain", message)
    mail = Mail(os.environ.get('SENDGRID_EMAIL'), recipient, subject, content)

    sg.client.mail.send.post(request_body=mail.get())
    # Insert log: [EMAIL] "timestamp" "email sent status" "ip address"

