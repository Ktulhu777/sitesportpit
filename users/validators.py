from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError
from django.contrib.auth.password_validation import validate_password as valid_passwd
from re import fullmatch
from datetime import datetime


class ValidateBasics:
    help_text_phone = 'Шаблоны номера телефона: "+7(XXX)-xxx-xx-xx"; +7XXXxxxxxxx; 8(XXX)-xxx-xx-xx'

    def validate_phone(self, attrs):
        old_phone = attrs[:]
        if attrs == old_phone:
            return attrs
        elif '+7' not in attrs[0:2]:
            raise ValidationError('Номер должен начинаться с "+7" ')
        elif not fullmatch(r'\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}|8\(\d{3}\)-\d{3}-\d{2}-\d{2}|\+7\d{10}', attrs):
            raise ValidationError('Номер не соответствует шаблону')
        elif get_user_model().objects.filter(phone=attrs).exists():
            raise ValidationError('Такой номер телефона уже существует')
        return attrs

    def validate_email(self, attrs):
        if get_user_model().objects.filter(email=attrs).exists():
            raise ValidationError('Такой E-mail уже существует')
        return attrs

    def validate_password(self, attrs):
        if valid_passwd(attrs) is None:
            return attrs

    def validate_date_birth(self, attrs):
        if not 1940 <= attrs.year < datetime.today().year:
            raise ValidationError('Укажите правильный год рождения')
        return attrs
