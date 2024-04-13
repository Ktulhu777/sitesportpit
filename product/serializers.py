from rest_framework import serializers
from .models import Product, CategoryProduct, Review


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'img', 'discount',
                  'discount_price', 'time_create', 'category', 'avg_rating',)

    def get_img(self, obj):
        if obj.img:
            return obj.img.url


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ('cat_name',)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ("id", "user", "review", "product_review", "create_date", "changes", "rating")

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.review = validated_data.get("review", instance.review)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.changes = True
        instance.save()
        return instance
