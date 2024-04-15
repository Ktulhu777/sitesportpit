from rest_framework import serializers
from product.models import Product
from product.serializers import ProductImagesSerializer


class CartSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'discount_price',
                  'discount', 'images',)
