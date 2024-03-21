from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(label='Номер телефона')
    email = serializers.CharField(label='Электронная почта')

    class Meta:
        model = get_user_model()
        fields = ['username', 'phone_number', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    phone_number=validated_data['phone_number'],
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

