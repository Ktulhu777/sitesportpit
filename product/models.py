from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Product.Status.PUBLISHED)


class Product(models.Model):
    """Основная модель товара(продукта)"""

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField('Название продукта', max_length=150, db_index=True)

    slug = models.SlugField(
        'Slug(Формируется автоматически)',
        max_length=255, blank=True, unique=True
    )
    description = models.TextField('Описание', blank=True)
    is_published = models.BooleanField('Опубликовано', default=Status.PUBLISHED)
    price = models.FloatField('Цена', blank=True, default=100)
    discount_price = models.FloatField('Цена со скидкой', blank=True, default=0, null=True)

    time_create = models.DateTimeField('Дата создания', auto_now_add=True)
    time_update = models.DateTimeField('Дата обновления статьи', auto_now=True)

    category = models.ForeignKey(
        'CategoryProduct', on_delete=models.CASCADE, null=True,
        related_name='product', verbose_name='Категории'
    )
    quantity = models.PositiveIntegerField('Количество', default=0)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-time_create']

    def __str__(self):
        return self.name

    def get_category(self):
        return self.category.cat_name

    def avg_rating(self):
        if hasattr(self, '_avg_rating'):
            return self._avg_rating
        return self.review.aggregate(Avg('rating'))

    def discount(self):
        if self.discount_price:
            return round((self.price - self.discount_price) / self.price * 100, 2)
        return None


class CategoryProduct(models.Model):
    """Основная модель категорий"""
    cat_name = models.CharField('Категория', max_length=255, db_index=True)

    slug = models.SlugField(
        'Slug (Формируется автоматически)', max_length=255, unique=True
    )

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

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name='review', verbose_name='Пользователь'
    )

    review = models.TextField('Отзыв', blank=True, null=True)
    create_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    changes = models.BooleanField('Изменено', default=False)

    product_review = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='review', verbose_name='Товар', null=True
    )

    rating = models.IntegerField(
        'Оценка', blank=True,
        null=True, choices=RatingChoice.choices
    )

    objects = models.Manager()

    class Meta:
        ordering = ('-create_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Пользователь: {self.user}, товар: {self.product_review}, оценка: {self.rating}'


def product_image_directory_path(instance, filename):
    """Метод для сохранения фотографий по нужному пути"""
    return f'product_photo/{instance.product.category}/{instance.product.slug}/{filename}'


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images', verbose_name='Товар'
    )

    image = models.ImageField('Изображение', upload_to=product_image_directory_path)

    def __str__(self):
        return f'Товар: {self.product.name}'


class LikeProduct(models.Model):
    """Класс лайков продуктов"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='like')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='like')
    like = models.BooleanField('Лайк', default=False)

    objects = models.Manager()

