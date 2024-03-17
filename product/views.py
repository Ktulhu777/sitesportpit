
from django.http import HttpResponse
from rest_framework import viewsets, generics
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(generics.ListAPIView):
    """Клас для просмотра списка товаров либо просмотр одного"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if not slug:
            return Product.objects.all()
        return Product.objects.filter(slug=slug)


def home(request):
    return HttpResponse('<h1>Главная пробная старница</h1>')
