from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = (
        'user', 'city', 'street', 'house',
        'quantity_product', 'product', 'time_create_order', 'price', 'get_user_contact'
    )
    readonly_fields = ('time_create_order', 'price', 'get_user_contact')
    ordering = ('-time_create_order', 'product',)
    list_display = ('user', 'product', 'time_create_order')
    save_on_top = True

    @admin.display(description="Контакты заказчика", ordering='user')
    def get_user_contact(self, obj: Order):
        user = get_user_model().objects.get(username=obj.user)
        return f"[ {user.phone} ]; [ {user.email} ]"
