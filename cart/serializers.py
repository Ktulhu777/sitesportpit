from rest_framework import serializers
from product.models import Product
from .models import Order
from product.serializers import ProductImagesSerializer


class CartSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'price', 'discount_price',
            'discount', 'images',
        )


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        read_only_fields = ('time_create_order', )
        fields = (
            'user', 'city', 'street', 'house', 'quantity_product', 'product', 'price', 'time_create_order',
        )
