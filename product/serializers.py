from rest_framework import serializers
from .models import Product, CategoryProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'content', 'price', 'time_create', 'cat_id')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ('cat_name', )
