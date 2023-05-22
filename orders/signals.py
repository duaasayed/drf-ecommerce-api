from django.dispatch import receiver, Signal
from django.db.models.signals import post_save
from .models import OrderChangeHistory, Order
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Order)
def place_order(sender, instance, created, **kwargs):
    if instance.status == 0:
        subject = 'Thank you for your order!'
        template = 'emails/order_placed.html'
        customer = instance.customer
        context = {
            'order': {
                'no': instance.id,
                'total': instance.total_price,
                'payment': instance.get_payment_method_display(),
                'date': instance.placed_at,
                'address': instance.address
            },
            'customer': {
                'first_name': customer.first_name,
                'full_name': customer.get_full_name()
            }
        }
        _send_email(customer, subject, template, context)


@receiver(post_save, sender=OrderChangeHistory)
def track_order(sender, instance, created, **kwargs):
    if instance.status in [1, 4, 5]:
        customer = instance.order.customer
        template = ''
        subject = ''
        context = {
            'order': {
                'no': instance.order.id,
                'total': instance.order.total_price,
                'payment': instance.order.get_payment_method_display(),
                'address': instance.order.address
            },
            'customer': {
                'first_name': customer.first_name,
                'full_name': customer.get_full_name()
            }
        }

        if instance.status == 1:
            instance.order.status = 2
            template = 'emails/order_shipped.html'
            subject = 'Your item has been shipped!'
            context['shipoment_date'] = instance.created_at

        elif instance.status == 4:
            instance.order.status = 3
            template = 'emails/order_out_of_delivery.html'
            subject = 'Items from your order are out of delivery'

        elif instance.status == 5:
            instance.order.status = 4
            template = 'emails/order_delivered.html'
            subject = 'Your order has been delivered!'

        instance.order.save()
        _send_email(customer, subject, template, context)
    elif instance.status == 0:
        instance.order.status = 1
        instance.order.save()


def _send_email(user, subject, template, context):
    body = render_to_string(template, context)

    msg = EmailMultiAlternatives(
        subject, body, f'E-commerce <{settings.EMAIL_HOST_USER}>', [user.email])

    msg.attach_alternative(body, "text/html")
    msg.send()
