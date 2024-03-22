from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
