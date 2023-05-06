from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from accounts.models.custom_users import Customer
from accounts.models.base_user import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .services import calc_cosine_similarity
from datetime import datetime, timedelta


one_week_ago = datetime.now() - timedelta(days=7)


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def categories(self):
        return set([product.category for product in self.products.all()])

    @property
    def stores(self):
        return set([product.store for product in self.products.all()])


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL,
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
        return Product.objects.select_related('brand', 'category', 'store')\
            .prefetch_related('images', 'reviews').annotate(reviews_count=models.Count('reviews'))\
            .filter(category__in=self.get_descendants(include_self=True))

    @property
    def brands(self):
        return Brand.objects.filter(products__category__in=self.get_descendants(include_self=True)).distinct()

    @property
    def stores(self):
        return Store.objects.filter(products__category__in=self.get_descendants(include_self=True)).distinct()

    @property
    def best_sellers(self):
        return self.all_related_products \
            .annotate(order_count=models.Count('orderproduct'))\
            .filter(order_count__gt=0).order_by('-order_count')[:10]

    @property
    def new_arrivals(self):
        return self.all_related_products.order_by('-added_at')[:10]


class Store(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=300, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @ property
    def categories(self):
        return set([product.category for product in self.products.all()])

    @ property
    def brands(self):
        return set([product.brand for product in self.products.all()])


class Product(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, related_name='products')
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

    @ property
    def rating(self):
        total = 0
        for review in self.reviews.all():
            total += review.stars
        return total / self.reviews_count if self.reviews_count > 0 else 0

    @ property
    def related_products(self):
        # [store, brand, category, price]
        attrs_vector = [1, 1, 1, self.price]
        other = Product.objects.select_related(
            'store', 'brand', 'category').prefetch_related('images', 'reviews').exclude(id=self.id)
        similarities = []
        for p in other:
            p_vector = [0, 0, 0, p.price]
            if p.store_id == self.store_id:
                p_vector[0] = 1
            if p.brand_id == self.brand_id:
                p_vector[1] = 1
            if p.category_id == self.category_id:
                p_vector[2] = 1

            sim = calc_cosine_similarity(attrs_vector, p_vector)
            similarities.append((sim, p))

        similarities.sort(key=lambda x: float(x[0]), reverse=True)
        return [i[1] for i in similarities][:5]


def upload_to(instance, filename):
    return f'products/{instance.product.store.slug}/{instance.product.slug}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to)

    class Meta:
        db_table = 'shop_products_images'

    @ property
    def url(self):
        return self.image.url


def get_anonymous_user():
    user, created = User.objects.get_or_create(
        first_name='Deleted', last_name='User', email='deleted@user.com')
    if created:
        user.set_password('password')
    return user


class Review(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET(get_anonymous_user))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.CharField(max_length=250)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])


class Question(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET(get_anonymous_user))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='questions')
    content = models.CharField(max_length=250)

    @ property
    def answered(self):
        return self.answers.count() > 0


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET(get_anonymous_user))
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    content = models.CharField(max_length=250)

    @ property
    def verified(self):
        return self.user.is_store_representative and self.user.storerepresentative.store == self.question.product.store
