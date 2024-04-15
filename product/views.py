from django.db.models import Count, Avg
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from .filters import ProductFilter
from rest_framework import generics, status, mixins
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class ProductPagination(PageNumberPagination):
    """Класс пагинации"""
    page_size = 9
    page_size_query_param = 'page_size'  # пользователь сам регулирует вывод товаров &page_size=
    max_page_size = 100


class ProductAllView(generics.ListAPIView):
    """Класс для просмотра списка товаров с пагинацией """
    queryset = Product.published.annotate(_avg_rating=Avg('review__rating')
                                          ).all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    pagination_class = ProductPagination


class ProductDetailView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_slug = self.kwargs.get('product_slug')
        return Product.published.annotate(_avg_rating=Avg('review__rating')
                                          ).filter(slug=product_slug)


class ReviewProductView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        if self.kwargs.get('product_slug'):
            return Review.objects.filter(product_review__slug=self.kwargs.get('product_slug')
                                         ).select_related('user')


class ReviewProductChangesView(mixins.CreateModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               GenericViewSet):
    serializer_class = ReviewSerializerUpdateAndCreateSerializer
    queryset = Review.objects.all()


class CategoryProductView(generics.ListAPIView):
    """Класс категорий"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        Функция выводит все категории(у которых есть 1 и больше записей)
        если не указан после '/' slug
        """
        slug = self.kwargs.get('slug')
        if not slug:
            return CategoryProduct.objects.annotate(total=Count('product')
                                                    ).filter(total__gt=0)
        return CategoryProduct.objects.filter(slug=slug)


class IDProduct(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Product.published.annotate(_avg_rating=Avg('review__rating')
                                          ).filter(id=pk)


class LikeProductViews(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = LikeProductSerializer
    queryset = LikeProduct.objects.all()

    def destroy(self, request, *args: tuple, **kwargs: dict) -> Response[dict, status]:
        product = self.get_object()
        product.delete()
        return Response({'delete': 'лайк удален'}, status=status.HTTP_200_OK)
