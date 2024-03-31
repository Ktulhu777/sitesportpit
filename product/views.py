from django.db.models import Count, Avg
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from .models import Product, CategoryProduct, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly


class ProductPagination(PageNumberPagination):
    """Класс пагинации"""
    page_size = 9
    page_size_query_param = 'page_size'  # пользователь сам регулирует вывод товаров &page_size=
    max_page_size = 100


class ProductAllView(generics.ListAPIView):
    """Класс для просмотра списка товаров с пагинацией """
    queryset = Product.published.annotate(_avg_rating=Avg('review__rating')).all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductDetailView(APIView):
    """Класс для просмотра товара и отзывов на одной странице """
    permission_classes = (IsOwnerOrReadOnly, )

    def get(self, request, product_slug=None):
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

            return Response({"review": serializer.data})
        except:
            return Response({"error": "отзыв не добавлен"})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Данного отзыва не существует"})
        try:
            instance = Review.objects.get(pk=pk)
        except:
            return Response({"error": "Данного отзыва не существует"})

        serializer = ReviewSerializer(data=request.data, instance=instance, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"review": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Данного отзыва не существует"})
        try:
            instance = Review.objects.get(pk=pk)
        except:
            return Response({"error": "Данного отзыва не существует"})

        instance.delete()
        return Response({"review": "Отзыв успешно удален"})


class SearchProduct(generics.ListAPIView):
    """Класс для поиска товаров"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.published.filter(title__contains=self.request.GET.get('search'))


class CategoryProductView(generics.ListAPIView):
    """Класс категорий"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        """Функция выводит все категории(у которых есть 1 и больше записей) если не указан после '/' slug"""
        slug = self.kwargs.get('slug')
        if not slug:
            return CategoryProduct.objects.annotate(total=Count("product")).filter(total__gt=0)
        return CategoryProduct.objects.filter(slug=slug)


def home(request):
    return HttpResponse('<h1>Главная пробная старница</h1>')

#test