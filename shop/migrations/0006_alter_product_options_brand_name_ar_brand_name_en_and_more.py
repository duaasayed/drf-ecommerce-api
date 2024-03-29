# Generated by Django 4.1.7 on 2023-05-09 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_product_description_en_product_title_en"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "Product", "verbose_name_plural": "Products"},
        ),
        migrations.AddField(
            model_name="brand",
            name="name_ar",
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="name_en",
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="slug_ar",
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="brand",
            name="slug_en",
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="category",
            name="name_ar",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="name_en",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="slug_ar",
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="category",
            name="slug_en",
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="product",
            name="slug_ar",
            field=models.SlugField(max_length=600, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="product",
            name="slug_en",
            field=models.SlugField(max_length=600, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="store",
            name="name_ar",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="store",
            name="name_en",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="store",
            name="slug_ar",
            field=models.SlugField(max_length=300, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="store",
            name="slug_en",
            field=models.SlugField(max_length=300, null=True, unique=True),
        ),
    ]
