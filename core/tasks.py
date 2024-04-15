from django.core.mail import send_mail

from account.send_mail import send_confirm_email
from .celery import app


@app.task
def send_confirm_email_task(user, code):
    send_confirm_email(user, code)

@app.task
def send_notification_task(user, order_id, price):
    send_mail(
        'Order Notification!',
        f'''You ordered #{order_id}, \nWait for the call!\n
        Price: {price}.
        Thank you for staying with us!''',
        'dianataalaibekova2002@gmail.com',
        [user]
    )
