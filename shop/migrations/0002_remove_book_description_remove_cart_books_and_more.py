# Generated by Django 4.2.16 on 2024-09-10 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="description",
        ),
        migrations.RemoveField(
            model_name="cart",
            name="books",
        ),
        migrations.RemoveField(
            model_name="order",
            name="books",
        ),
        migrations.RemoveField(
            model_name="order",
            name="shipping_address",
        ),
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="book",
            name="genre",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="book",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="book",
            name="ratings",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=3, null=True
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="stock",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="book",
            name="title",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="shop.cart",
            ),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="quantity",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.PositiveIntegerField(),
        ),
    ]
