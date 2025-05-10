# In your app's signals.py
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.signals import password_reset


@receiver(password_reset)
def send_custom_reset_email(sender, user, **kwargs):
    send_mail(
        "Password Reset Requested",
        f"Hello {user.username},\n\nUse this link to reset your password: ...",
        "mkekae@gmail.com",
        [user.email],
        html_message="<p>HTML email version here</p>",
    )
