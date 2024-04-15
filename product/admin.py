from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, CategoryProduct, Review, Order, ProductImages


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImages


@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    fields = ('name', 'slug', 'description', 'is_published', 'price', 'discount_price', 'category', 'quantity')
    ordering = ('-time_create', 'name',)
    # readonly_fields = ('product_img',)
    list_display = ('name', 'time_create', 'is_published', 'category')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
    inlines = (GalleryInline,)

    # @admin.display(description="Изображение", ordering='description')
    # def product_img(self, product: Product):
    #     """Функция вывода изображения, если оно есть"""
    #     if product.img:
    #         return mark_safe(f"<img src='{product.img.url}' width=50>")
    #     return "Без фото"


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


admin.site.register(Order)
