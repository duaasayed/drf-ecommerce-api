from django.dispatch import receiver
from django.db.models.signals import post_save
from .models.custom_users import Customer
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import email_verification_token
from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Customer)
def verify_email(sender, instance, created, **kwargs):
    if created:
        current_domain = settings.DEV_DOMAIN
        subject = 'Activate Your Account'
        body = render_to_string(
            'emails/email_verification.html',
            {
                'domain': current_domain,
                'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                'token': email_verification_token.make_token(instance),
            }
        )

        msg = EmailMultiAlternatives(
            subject, body, f'E-commerce <{settings.EMAIL_HOST_USER}>', [instance.email])

        msg.attach_alternative(body, "text/html")
        msg.send()
