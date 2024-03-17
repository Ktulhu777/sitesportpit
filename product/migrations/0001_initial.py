# Generated by Django 5.0.3 on 2024-03-17 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(db_index=True, max_length=255, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug (Формируется автоматически)')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название продукта')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug (Формируется автоматически)')),
                ('content', models.TextField(blank=True, verbose_name='Описание')),
                ('is_published', models.BooleanField(default=1)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=100, max_digits=10, verbose_name='Цена')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления статьи')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-time_create'],
            },
        ),
    ]
