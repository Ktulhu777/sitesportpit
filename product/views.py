import time

from cloudipsp import Api, Checkout
from django.db.models import Count, Avg, Q
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import Product, CategoryProduct, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, OrderSerializer

from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    """Класс пагинации"""
    page_size = 9
    page_size_query_param = 'page_size'  # пользователь сам регулирует вывод товаров &page_size=
    max_page_size = 100


class ProductAllView(generics.ListAPIView):
    """Класс для просмотра списка товаров с пагинацией """
    queryset = Product.published.annotate(_avg_rating=Avg('review__rating')).all()
    serializer_class = ProductSerializer
    # pagination_class = ProductPagination


class ProductDetailView(APIView):
    """Класс для просмотра товара и отзывов на одной странице """
    permission_classes = IsOwnerOrReadOnly,

    def get(self, request, product_slug):
        product = Product.published.annotate(_avg_rating=Avg('review__rating')).filter(slug=product_slug)
        review = Review.objects.filter(product_review__slug=product_slug).select_related('user')

        return Response({"product": ProductSerializer(product, many=True).data,
                         "review": ReviewSerializer(review, many=True).data})

    def post(self, request, product_slug):
        try:
            product = Product.published.get(slug=product_slug)
            request.data["product_review"] = product.pk
            serializer = ReviewSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"review": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "отзыв не добавлен"}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if not pk:
            return Response({"error": "Данного отзыва не существует"})

        try:
            instance = Review.objects.get(pk=pk)
            self.check_object_permissions(request, instance)
        except:
            return Response({"detail": "Данный отзыв нельзя изменить"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerializer(data=request.data, instance=instance, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"review": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Данного отзыва не существует"})
        try:
            instance = Review.objects.get(pk=pk)
            self.check_object_permissions(request, instance)
        except:
            return Response({"detail": "Данный отзыв нельзя удалить"}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response({"review": "Отзыв успешно удален"}, status=status.HTTP_200_OK)


class SearchProduct(generics.ListAPIView):
    """Класс для поиска товаров"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.published.filter(name__contains=self.request.GET.get('search'))


class CategoryProductView(generics.ListAPIView):
    """Класс категорий"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        """Функция выводит все категории(у которых есть 1 и больше записей) если не указан после '/' slug"""
        slug = self.kwargs.get('slug')
        if not slug:
            return CategoryProduct.objects.annotate(total=Count("product")).filter(total__gt=0)
        return CategoryProduct.objects.filter(slug=slug)


class OrderView(APIView):
    def post(self, request):
        order = OrderSerializer(data=request.data)
        if order.is_valid():
            order.save()
            api = Api(merchant_id=1396424,
                      secret_key='test')
            checkout = Checkout(api=api)
            data = {
                "currency": "RUB",
                "amount": round(int(request.data['summa']), 2),
                "order_descr": 'Оплата товаров',
                "order_time": str(time.time()),
            }
            url = checkout.url(data).get('checkout_url')
            return Response({'result': 'Пожалуйста подождите...', 'url': url})
        return Response({'result': 'Ошибка в форме'})
