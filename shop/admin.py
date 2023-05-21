from django.contrib import admin
from .models import Product, Category, Brand, Store, ProductSpecification
from modeltranslation.admin import TranslationAdmin


class ProductsAdmin(TranslationAdmin):
    pass


class CategoryAdmin(TranslationAdmin):
    pass


class ProductSpecAdmin(TranslationAdmin):
    list_display = ('product', 'spec', 'value')


# Register your models here.
admin.site.register(Product, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Store)
admin.site.register(ProductSpecification, ProductSpecAdmin)
