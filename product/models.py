from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Product.Status.PUBLISHED)


class Product(models.Model):
    """Основная модель товара(продукта)"""

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(max_length=150, verbose_name='Название продукта')
    slug = models.SlugField(max_length=255, blank=True,
                            unique=True, verbose_name='Slug (Формируется автоматически)')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_published = models.BooleanField(default=Status.PUBLISHED)
    price = models.FloatField(blank=True, default=100, verbose_name='Цена')
    discount = models.IntegerField(blank=True, null=True, default=0, verbose_name='Скидка')
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                            blank=True, null=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления статьи')
    cat = models.ForeignKey('CategoryProduct', on_delete=models.CASCADE, null=True,
                            related_name='posts', verbose_name="Категории")
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    # tags = models.ManyToManyField('Tags', blank=True, related_name='tags', verbose_name="Теги")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-time_create']

    def save(self, *args, **kwargs):
        """Формирует автомачески slug для продукта"""
        transliterated_name = unidecode(str(self.name))
        self.slug = slugify(transliterated_name)
        super().save(*args, **kwargs)


class CategoryProduct(models.Model):
    """Основная модель категорий"""
    cat_name = models.CharField(max_length=255, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug (Формируется автоматически)')

    objects = models.Manager()

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

# => В ОБДУМКЕ !
# class Review(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='product')
#     review = models.TextField(blank=True, verbose_name='Отзыв', null=True)
#     product_review = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     objects = models.Manager()
#
#     def __str__(self):
#         return self.review
#
#     class Meta:
#         verbose_name = 'Отзыв'
#         verbose_name_plural = 'Отзывы'

# class UploadFiles(models.Model):
#     file = models.FileField(upload_to='uploads_model')
