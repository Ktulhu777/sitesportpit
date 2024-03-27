from rest_framework import serializers
from .models import Product, CategoryProduct


class ProductSerializer(serializers.ModelSerializer):
    cat = serializers.CharField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'img', 'price', 'discount', 'time_create', 'cat')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ('cat_name',)
