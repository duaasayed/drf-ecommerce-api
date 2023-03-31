from django.db import models
from shop.models import Product
from accounts.models.custom_users import Customer


class Cart(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name='cart',)
    products = models.ManyToManyField(Product, through='CartProduct')

    @property
    def total_price(self):
        total = 0
        for product in self.cart_products.select_related('product').all():
            total += product.total_price
        return total

    def has_product(self, product):
        return product in self.products.all()

    def clear(self):
        self.cart_products.all().delete()


class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts_cart_products'
        constraints = [
            models.UniqueConstraint(
                'product', 'cart', name='unique_cart_product')
        ]

    @property
    def price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.price * self.quantity
