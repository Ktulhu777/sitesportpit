from rest_framework import serializers
from .models import Product, CategoryProduct, Review, ProductImages, LikeProduct
from .validators import ValidateBasics


class ProductImagesSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = ProductImages
        fields = ('img',)

    def get_img(self, obj):
        if obj.image:
            return obj.image.url


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug','category', 'price', 'discount_price', 'discount', 'images')


class ProductDetailSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'price', 'discount_price',
                  'discount', 'quantity', 'time_create', 'images')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ('cat_name',)


class ReviewSerializer(serializers.ModelSerializer, ValidateBasics):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'user', 'review', 'product_review', 'create_date', 'changes', 'rating')


class ReviewSerializerUpdateAndCreateSerializer(ReviewSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        instance.review = validated_data.get('review', instance.review)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.changes = True
        instance.save()
        return instance


class LikeProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LikeProduct
        fields = ('id', 'user', 'product', 'like')

    def create(self, validated_data):
        validated_data['like'] = True
        return LikeProduct.objects.create(**validated_data)
