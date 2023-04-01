from django.db import models
from accounts.models.custom_users import Customer


class AddressBook(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='addresses')
    phone = models.CharField(max_length=11)
    governorate = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    building = models.CharField(max_length=50)
    floor = models.CharField(max_length=50)
    landmark = models.CharField(max_length=150, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles_address_book'
        verbose_name_plural = 'Address Book'
