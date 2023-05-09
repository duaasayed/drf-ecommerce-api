from modeltranslation.translator import translator, TranslationOptions
from . import models


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')


translator.register(models.Category, CategoryTranslationOptions)
translator.register(models.Product, ProductTranslationOptions)
