# Generated by Django 4.1.5 on 2024-04-13 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(blank=True, default=models.FloatField(blank=True, default=100, verbose_name='Цена'), null=True, verbose_name='Цена со скидкой'),
        ),
    ]
