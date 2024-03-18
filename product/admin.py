from django.contrib import admin
from .models import Product, CategoryProduct


@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    fields = ('title', 'content', 'is_published', 'price', 'cat')
    ordering = ['-time_create', 'title']
    save_on_top = True


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    fields = ('cat_name', 'slug',)
    prepopulated_fields = {"slug": ("cat_name",)}
