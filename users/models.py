from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # class Genders(models.TextChoices):
    #     MALE = 'M', 'Мужчина'
    #     FEMALE = 'F', 'Женщина'
    #     UNDEFINED = 'U', 'Не выбран'
    #
    # date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    # gender = models.CharField(max_length=1, choices=Genders.choices, default=Genders.UNDEFINED, verbose_name='Пол')
    #
    # def __str__(self):
    #     return self.username
