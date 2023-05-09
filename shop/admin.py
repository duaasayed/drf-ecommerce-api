from django.contrib import admin
from .models import Product, Category, Brand, Store
from modeltranslation.admin import TranslationAdmin


class ProductsAdmin(TranslationAdmin):
    pass


class CategoryAdmin(TranslationAdmin):
    pass


# Register your models here.
admin.site.register(Product, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Store)
