# Generated by Django 4.2.16 on 2024-09-16 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_order_address_order_city_order_full_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="book_images/"),
        ),
    ]
