from django.db.models import Count
from django.http import HttpResponse
from rest_framework import generics
from .models import Product, CategoryProduct
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(generics.ListAPIView):
    """Клас для просмотра списка товаров либо просмотр одного"""
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if not slug:
            return Product.objects.all()
        return Product.objects.filter(slug=slug)


class SearchProduct(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.published.filter(title__contains=self.request.GET.get('search'))


class CategoryProductView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if not slug:
            return CategoryProduct.objects.annotate(total=Count("posts")).filter(total__gt=0)
        return CategoryProduct.objects.filter(slug=slug)


def home(request):
    return HttpResponse('<h1>Главная пробная старница</h1>')
