from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Customer(UserModel):
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True)

    def has_purchased(self, product):
        return self.orders.filter(products__id=product).exists()


class Staff(UserModel):
    seller = models.ForeignKey(
        'shop.Seller', on_delete=models.CASCADE, related_name='staff')
    is_admin = models.BooleanField(default=False)
    added_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'sellers_staff'
        verbose_name_plural = 'Staff'

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)
