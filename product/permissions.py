from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Класс предоставления доступа к объектам класса Review
    """

    def has_object_permission(self, request, view, obj):
        """Если запрос безопа́сный - выдает данные на чтение, если запрос не безопасный,
        то происходит проверка, имеет ли отношение пользователя к данному объекту класса"""
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return True
        return request.user == obj.user
