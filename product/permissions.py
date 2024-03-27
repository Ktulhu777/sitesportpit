from rest_framework import permissions
from .models import Product, Review


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Класс предоставления доступа к объектам класса Review
    """

    def has_object_permission(self, request, view, obj):
        """Если запрос безопа́сный то выдает данные на чтение, если запрос не безопасный,
        то происходит проверка, имеет ли отношение пользователя к данному объекту класса"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user