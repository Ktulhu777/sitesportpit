from rest_framework import serializers
from .models import Product, CategoryProduct, Review, Order, ProductImages


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
    img = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'img', 'discount_price',
                  'discount', 'time_create', 'category', 'avg_rating', 'images',)

    def get_img(self, obj):
        if obj.img:
            return obj.img.url



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ('cat_name',)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
