from django.contrib import admin
from .models import Product, CategoryProduct

admin.site.register(Product)


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    fields = ('cat_name', 'slug',)
    prepopulated_fields = {"slug": ("cat_name",)}


