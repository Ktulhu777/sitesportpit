from rest_framework import serializers
from .models import Product, CategoryProduct, Review, Order, ProductImages, LikeProduct
from .validators import ValidateBasicsLike

class ProductImagesSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = ProductImages
        fields = ('id', 'img')

    def get_img(self, obj):
        if obj.image:
            return obj.image.url


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'discount_price',
                  'discount', 'time_create', 'category', 'avg_rating', 'images',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ('cat_name',)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ("id", "user", "review", 'product_review', "create_date", "changes", "rating")

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.review = validated_data.get("review", instance.review)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.changes = True
        instance.save()
        return instance


class LikeProductSerializer(serializers.ModelSerializer, ValidateBasicsLike):
    class Meta:
        model = LikeProduct
        fields = ('id', 'user', 'product', 'like')

    def create(self, validated_data):
        return LikeProduct.objects.create(**validated_data)