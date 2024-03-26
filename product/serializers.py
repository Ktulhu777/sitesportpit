from rest_framework import serializers
from .models import Product, CategoryProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'img', 'price', 'discount', 'time_create', 'cat_name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ('cat_name', )
