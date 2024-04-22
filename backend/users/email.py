import random
import string
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_email(email, otp):
    print(f"This is the email {email}")
    subject = 'Your OTP for Login'
    message = f'Your OTP is: {otp}'
    print(subject)
    print(message)
    from_email = settings.EMAIL_HOST_USER
    print(from_email)
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)