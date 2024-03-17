from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from unidecode import unidecode


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Product.Status.PUBLISHED)


class Product(models.Model):
    """Основная модель товара(продукта)"""

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=150, verbose_name='Название продукта')
    slug = models.SlugField(max_length=255, blank=True,
                            unique=True, verbose_name='Slug (Формируется автоматически)')
    content = models.TextField(blank=True, verbose_name='Описание')
    is_published = models.BooleanField(default=Status.PUBLISHED)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                blank=True, default=100, verbose_name='Цена')
    # photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
    #                           blank=True, null=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления статьи')

    cat = models.ForeignKey('CategoryProduct', on_delete=models.CASCADE, null=True,
                            related_name='posts', verbose_name="Категории")
    # tags = models.ManyToManyField('Tags', blank=True, related_name='tags', verbose_name="Теги")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        """Формирует автомачески slug для продукта"""
        transliterated_title = unidecode(str(self.title))
        self.slug = slugify(transliterated_title)
        super().save(*args, **kwargs)


class CategoryProduct(models.Model):
    cat_name = models.CharField(max_length=255, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug (Формируется автоматически)')

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
        