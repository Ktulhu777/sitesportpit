from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User
from .validators import ValidateBasics


class UserSerializer(serializers.ModelSerializer):
    help_text = "Обязательное уникальное поле. Не более 20 символов. Только буквы, цифры и символ ' _ ' "

    username = serializers.CharField(min_length=2, max_length=20,
                                     help_text=help_text)
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


class ProfileSerializer(serializers.ModelSerializer, ValidateBasics):
    # phone = serializers.CharField(required=False, max_length=14, help_text="Формат номера: +7(XXX)-XXX-XX-XX")
    date_birth = serializers.DateTimeField(required=False, input_formats=None)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email", "date_birth", "city"]
        read_only_fields = ("id", "username", "email")
