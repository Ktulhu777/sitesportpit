from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}

        return serializer_class(*args, **kwargs)

    def activation(self, request, *args, **kwargs):
        try:
            super().activation(request, *args, **kwargs)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
