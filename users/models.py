from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_photo = models.ImageField(upload_to='user_photos/%Y/%m/%d/', default=None,
                                   blank=True, null=True, verbose_name='Фото пользователя')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания учетной записи')
    phone = models.CharField(blank=True, max_length=14, verbose_name='Номер телефона')
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    city = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.username

