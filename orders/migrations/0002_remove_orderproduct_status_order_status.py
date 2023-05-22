# Generated by Django 4.1.7 on 2023-05-22 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderproduct",
            name="status",
        ),
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.IntegerField(
                choices=[
                    (0, "Placed"),
                    (1, "Prepared"),
                    (2, "Shipped"),
                    (3, "Out for Delivery"),
                    (4, "Delivered"),
                ],
                default=0,
            ),
        ),
    ]