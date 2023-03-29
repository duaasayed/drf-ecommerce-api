from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='subcategories')
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    show_in_nav = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(
                'name', 'parent', name='unique_sub_categories')
        ]

    def __str__(self):
        return self.name

    @property
    def all_related_products(self):
        return Product.objects.select_related('brand', 'category', 'seller')\
            .prefetch_related('images').filter(category__in=self.get_descendants(include_self=True))


class Seller(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=300, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(
        Seller, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products')
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=600, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    available = models.BooleanField(default=True)
    in_stock = models.IntegerField(null=True)
    description = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def upload_to(instance, filename):
    return f'products/{instance.product.seller.slug}/{instance.product.slug}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to)

    class Meta:
        db_table = 'shop_products_images'

    @property
    def url(self):
        return self.image.url
