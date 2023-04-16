# Generated by Django 4.1.7 on 2023-04-16 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("shop", "0001_initial"),
        ("accounts", "0002_storerepresentative"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
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
                (
                    "customer",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart",
                        to="accounts.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CartProduct",
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
                ("quantity", models.IntegerField(default=1)),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart_products",
                        to="carts.cart",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.product"
                    ),
                ),
            ],
            options={
                "db_table": "carts_cart_products",
            },
        ),
        migrations.AddField(
            model_name="cart",
            name="products",
            field=models.ManyToManyField(
                through="carts.CartProduct", to="shop.product"
            ),
        ),
        migrations.AddConstraint(
            model_name="cartproduct",
            constraint=models.UniqueConstraint(
                models.F("product"), models.F("cart"), name="unique_cart_product"
            ),
        ),
    ]
