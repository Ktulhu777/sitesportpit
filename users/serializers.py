from django.contrib.auth import get_user_model
from rest_framework import serializers
from .validators import ValidateBasics
from djoser.serializers import UserCreatePasswordRetypeSerializer


class ProfileSerializer(serializers.ModelSerializer, ValidateBasics):
    phone = serializers.CharField(required=False, help_text=ValidateBasics.help_text_phone)
    date_birth = serializers.DateTimeField(required=False, input_formats=None)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'user_photo', 'username', 'first_name',
            'last_name', 'email', 'date_birth', 'city', 'phone'
        )

        read_only_fields = ('id', 'username', 'email')


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer, ValidateBasics):

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
