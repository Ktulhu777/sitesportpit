from django.contrib.auth import get_user_model
from django.db import models
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT,
                             related_name='order', verbose_name='Никнейм')

    city = models.CharField('Город', max_length=50)
    street = models.CharField('Улица', max_length=50)
    house = models.CharField('Номер дома', max_length=20)
    quantity_product = models.IntegerField('Количество заказанного товара')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT,
                                related_name='order', verbose_name='Товар')

    price = models.IntegerField('Общая сумма товаров')
    time_create_order = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField('Статус заказа', default=False)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['time_create_order']

    def __str__(self):
        return f'Покупатель: {self.user}; Дата оформления заказа: {self.time_create_order}'
