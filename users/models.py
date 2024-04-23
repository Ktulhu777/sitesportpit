from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_photo = models.ImageField(
        'Фото пользователя', upload_to='user_photos/%Y/%m/%d/',
        default=None, blank=True, null=True
    )

    date_joined = models.DateTimeField('Дата создания учетной записи', auto_now_add=True)
    phone = models.CharField('Номер телефона', blank=True, max_length=14)
    date_birth = models.DateField('Дата рождения', blank=True, null=True)
    city = models.CharField('Город', blank=True, max_length=50)
    telegram_id = models.IntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.username
