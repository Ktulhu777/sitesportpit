# Generated by Django 4.1.5 on 2024-04-13 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_discount_price_product_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount',
            new_name='discount_price',
        ),
    ]
