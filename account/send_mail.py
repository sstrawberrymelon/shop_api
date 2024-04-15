from decouple import config
from django.core.mail import send_mail

HOST = config('HOST')

def send_confirm_email(user, code):
    link = f'{HOST}/api/v1/accounts/activate/{code}/'
    send_mail(
    'Hello, please activate your account',
        f'To activate your account enter a link bellow: \n{link}'
        f'\nLink works only one time!',
        f'dianataalaibekova2002@gmail.com',
        [user],
        fail_silently=False,
    )
