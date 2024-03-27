from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, CategoryProduct


@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    fields = ('name', 'description', 'img', 'product_img', 'is_published', 'price', 'cat')
    ordering = ('-time_create', 'name',)
    readonly_fields = ('product_img',)
    list_display = ('name', 'product_img', 'time_create', 'is_published', 'cat')
    list_display_links = ('name',)
    save_on_top = True

    @admin.display(description="Изображение", ordering='description')
    def product_img(self, product: Product):
        """Функция вывода изображения, если оно есть"""
        if product.img:
            return mark_safe(f"<img src='{product.img.url}' width=50>")
        return "Без фото"


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    fields = ('cat_name', 'slug',)
    prepopulated_fields = {"slug": ("cat_name",)}  # автоматически формирует слаг на основе cat_name
