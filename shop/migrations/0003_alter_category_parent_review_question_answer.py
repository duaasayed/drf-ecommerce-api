# Generated by Django 4.1.7 on 2023-04-08 18:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_staff"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0002_brand_product_productimage_seller_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="subcategories",
                to="shop.category",
            ),
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(max_length=250)),
                (
                    "stars",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=models.SET(shop.models.get_anonymous_user),
                        to="accounts.customer",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="shop.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(max_length=250)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=models.SET(shop.models.get_anonymous_user),
                        to="accounts.customer",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="shop.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(max_length=250)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="shop.question",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.SET(shop.models.get_anonymous_user),
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
