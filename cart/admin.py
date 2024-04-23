from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = (
        'user', 'city', 'street', 'house', 'quantity_product',
        'product', 'time_create_order', 'price', 'is_active', 'get_user_contact'
    )
    readonly_fields = (
        'user', 'city', 'street', 'house', 'quantity_product',
        'product', 'time_create_order', 'price', 'get_user_contact'
    )
    ordering = ('-time_create_order', 'product',)
    list_display = ('user', 'product', 'time_create_order')
    save_on_top = True

    @admin.display(description="Контакты заказчика", ordering='user')
    def get_user_contact(self, order: Order):
        return f'Номер телефона: [ {order.user.phone} ]; Email-адрес [ {order.user.email} ]'
