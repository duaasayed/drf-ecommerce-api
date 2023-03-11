from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from .models.custom_users import Customer
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import email_verification_token, password_reset_token
from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives


password_forgotten = Signal()


@receiver(post_save, sender=Customer)
def verify_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Activate Your Account'
        template = 'emails/email_verification.html'
        token_type = email_verification_token
        _send_token_email(instance, subject, template, token_type)


@receiver(password_forgotten)
def reset_password(sender, instance, **kwargs):
    subject = 'Reset Your Password'
    template = 'emails/password_reset.html'
    token_type = password_reset_token
    _send_token_email(instance, subject, template, token_type)


def _send_token_email(user, subject, template, token_type):
    body = render_to_string(
        template,
        {'name': user.first_name, 'domain': settings.DEV_DOMAIN, 'uid': urlsafe_base64_encode(
            force_bytes(user.pk)), 'token': token_type.make_token(user), 'header': subject}
    )

    msg = EmailMultiAlternatives(
        subject, body, f'E-commerce <{settings.EMAIL_HOST_USER}>', [user.email])

    msg.attach_alternative(body, "text/html")
    msg.send()
