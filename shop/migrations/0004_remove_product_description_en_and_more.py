# Generated by Django 4.1.7 on 2023-05-09 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_remove_product_description_af_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="description_en",
        ),
        migrations.RemoveField(
            model_name="product",
            name="title_en",
        ),
    ]
