from flask import current_app
from flask_mail import Message
from app import mail
from threading import Thread



def send_async_email(app_context, msg):
    app_context.push()
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app.app_context(), msg)).start()