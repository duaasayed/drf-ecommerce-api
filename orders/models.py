from django.db import models
from accounts.models.custom_users import Customer
from shop.models import Product
from profiles.models import AddressBook
from django.utils.translation import gettext as _


class Order(models.Model):
    PAYMENT_METHODS = (
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment')
    )
    STATUSES = (
        (0, 'Placed'),
        (1, 'Prepared'),
        (2, 'Shipped'),
        (3, 'Out for Delivery'),
        (4, 'Delivered')
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='orders')
    address = models.ForeignKey(AddressBook, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product, through='OrderProduct')
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
    status = models.IntegerField(default=0, choices=STATUSES)
    placed_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        COD_FEE = 12 if self.payment_method == 'COD' else 0
        TRANSFER_FEE = 20 if self.payment_method == 'ONLINE' else 0
        sub_total = 0

        for product in self.order_products.all():
            sub_total += product.total_price
        total = sub_total + COD_FEE + TRANSFER_FEE
        return total

    @property
    def can_be_canceled(self):
        return self.status >= 2


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # self.product.in_stock -= self.quantity
        # self.product.save()


class OrderChangeHistory(models.Model):
    STATUSES = (
        (0, _('Carrier picked up the package.')),
        (1, _('Package arrived at our facility')),
        (2, _('Package departed our facility')),
        (3, _('Package arrived at the final delivery station')),
        (4, _('Out for delivery')),
        (5, _('Delivered'))
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='history')
    location = models.CharField(
        _('location'), max_length=60, null=True, blank=True)
    status = models.IntegerField(_('status'), choices=STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.location} - {_(self.get_status_display())} at {self.created_at}'
