# Generated by Django 4.2.16 on 2024-09-12 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0003_alter_cartitem_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.CharField(default="Not Provided", max_length=255),
        ),
        migrations.AddField(
            model_name="order",
            name="city",
            field=models.CharField(default="Not Provided", max_length=100),
        ),
        migrations.AddField(
            model_name="order",
            name="full_name",
            field=models.CharField(default="Not Provided", max_length=255),
        ),
        migrations.AddField(
            model_name="order",
            name="postal_code",
            field=models.CharField(default="00000", max_length=20),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("shipped", "Shipped"),
                    ("delivered", "Delivered"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("book", "user")},
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("quantity", models.PositiveIntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.book"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="shop.order",
                    ),
                ),
            ],
        ),
    ]
