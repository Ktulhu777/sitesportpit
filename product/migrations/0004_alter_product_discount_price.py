# Generated by Django 5.0.4 on 2024-04-14 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Цена со скидкой'),
        ),
    ]
