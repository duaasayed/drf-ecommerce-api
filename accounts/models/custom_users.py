from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Customer(UserModel):
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True)

    def has_purchased(self, product):
        return self.orders.filter(products__id=product).exists()


class StoreRepresentative(UserModel):
    store = models.ForeignKey(
        'shop.Store', on_delete=models.CASCADE, related_name='representatives')
    is_admin = models.BooleanField(default=False)
    added_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'store_representatives'

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)
