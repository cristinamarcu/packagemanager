import smtplib
import ssl
from email.message import EmailMessage
from Config import SMTP_PASSWORD, SMTP_LOGIN, SMTP_SERVER


def build_message(apartment: str, name: str, description: str, date: str, action: str) -> str:
    message = f"Hi {name},\nThe package {description} for apartment {apartment}, on {date} was {action}.\nThank you."
    return message


def send_notification(receiver_email: str, apartment: str, name: str, description: str, date: str, action: str) -> bool:
    port = 465
    smtp_server = SMTP_SERVER
    login = SMTP_LOGIN
    password = SMTP_PASSWORD
    message = build_message(apartment, name, description, date, action)
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Package notification'
    msg['From'] = login
    msg['To'] = receiver_email
    context = ssl.create_default_context()
    valid = True
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(login, password)
            server.send_message(msg)
    except:
        valid = False
    return valid
