from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError
from django.contrib.auth.password_validation import validate_password as valid_passwd


class ValidateBasics:

    def validate_phone(self, attrs):
        if get_user_model().objects.filter(phone=attrs).exists():
            raise ValidationError("Такой номер телефона уже существует")
        elif "+7" not in attrs[0:2]:
            raise ValidationError("Номер должен начинаться с '+7' ")
        return attrs

    def validate_email(self, attrs):
        if get_user_model().objects.filter(email=attrs).exists():
            raise ValidationError("Такой E-mail уже существует")
        return attrs

    def validate_password(self, attrs):
        if valid_passwd(attrs) is None:
            return attrs
