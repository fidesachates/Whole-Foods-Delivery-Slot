import smtplib
import ssl
from email.message import EmailMessage

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "deliveryslotbob@gmail.com"
receiver_email = "you email here"
password = ""


def notify_slot_found(message):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(None, None, context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        msg = EmailMessage()
        msg['Subject'] = message
        msg['To'] = receiver_email
        msg['From'] = receiver_email
        msg.set_content("This message was automatically sent.")
        server.send_message(msg)
        server.quit()
