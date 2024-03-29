from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics
from .serializers import UserSerializer, ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    lookup_field = "username"

    def get_queryset(self):
        username = self.kwargs.get("username")
        if self.request.user.username == username:
            return get_user_model().objects.filter(username=username)