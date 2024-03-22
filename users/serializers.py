from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=2, max_length=20,
                                     help_text="Обязательное уникальное поле. Не более 20 символов. Только буквы, цифры и символ ' _ ' ")
    email = serializers.CharField(min_length=8, max_length=30, label='Электронная почта')

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_phone_number(self, attrs):
        if get_user_model().objects.filter(phone_number=attrs).exists():
            raise ValidationError("Такой номер телефона уже существует")
        return attrs

    def validate_email(self, attrs):
        if get_user_model().objects.filter(email=attrs).exists():
            raise ValidationError("Такой E-mail уже существует")
        return attrs

    def validate_password(self, attrs):
        if validate_password(attrs) is None:
            return attrs
