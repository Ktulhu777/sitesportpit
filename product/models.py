from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
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
    discount = models.PositiveIntegerField(blank=True, default=0, verbose_name='Скидка', null=True)
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                            blank=True, null=True, verbose_name="img")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления статьи')
    category = models.ForeignKey('CategoryProduct', on_delete=models.CASCADE, null=True,
                                 related_name='product', verbose_name="Категории")
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-time_create']

    def __str__(self):
        return self.name

    @property
    def get_category(self):
        return self.category.cat_name

    @property
    def avg_rating(self):
        if hasattr(self, '_avg_rating'):
            return self._avg_rating
        return self.review.aggregate(Avg('rating'))

    @property
    def discount_price(self):
        if self.discount:
            return round(self.price - (self.price / 100 * self.discount), 2)
        return None

    def save(self, *args, **kwargs):
        """Формирует автоматически slug для продукта"""
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


class Review(models.Model):
    class RatingChoice(models.IntegerChoices):
        one = 1, '★☆☆☆☆'
        two = 2, '★★☆☆☆'
        three = 3, '★★★☆☆'
        four = 4, '★★★★☆'
        five = 5, '★★★★★'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='review')
    review = models.TextField(blank=True, verbose_name='Отзыв', null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    changes = models.BooleanField(default=False)
    product_review = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review', null=True)
    rating = models.IntegerField(null=True, blank=True, verbose_name='Оценка', choices=RatingChoice.choices)
    objects = models.Manager()

    def __str__(self):
        return f'Пользователь: {self.user}, товар: {self.product_review}, оценка: {self.rating}'

    class Meta:
        ordering = ('-create_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Order(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=55, verbose_name='Фамилия')
    email = models.CharField(max_length=255, verbose_name='E-mail')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=20, verbose_name='Номер дома')
    basket = models.TextField(verbose_name='Корзина')

    def __str__(self):
        return f'{self.name} {self.surname} ({self.phone}) {self.email}'
