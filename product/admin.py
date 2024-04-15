from django.contrib import admin
from .models import Product, CategoryProduct, Review, ProductImages


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImages


@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    fields = (
        'name', 'slug', 'description', 'is_published',
        'price', 'discount_price', 'category', 'quantity'
    )
    ordering = ('-time_create', 'name',)
    list_display = ('name', 'time_create', 'is_published', 'category')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
    inlines = (GalleryInline,)


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    fields = ('cat_name', 'slug',)
    prepopulated_fields = {'slug': ('cat_name',)}  # автоматически формирует слаг на основе cat_name


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ('user', 'product_review', 'rating', 'review')
    ordering = ('-create_date', 'product_review', 'user', 'rating')
    list_display = ('user', 'product_review', 'rating', 'create_date')
    list_display_links = ('user', 'product_review')
    # readonly_fields = ('user', 'product_review', 'rating', 'review')
