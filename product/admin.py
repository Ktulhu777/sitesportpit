from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, CategoryProduct


@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    fields = ('title', 'content', 'photo', 'post_photo', 'is_published', 'price', 'cat')
    ordering = ('-time_create', 'title',)
    readonly_fields = ('post_photo',)
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    save_on_top = True

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, product: Product):
        if product.photo:
            return mark_safe(f"<img src='{product.photo.url}' width=50>")
        return "Без фото"


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    fields = ('cat_name', 'slug',)
    prepopulated_fields = {"slug": ("cat_name",)}
