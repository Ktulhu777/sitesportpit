from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': (
            'username', 'user_photo', 'first_name', 'last_name',
            'email', 'phone', 'date_birth', 'city', 'date_joined', 'telegram_id'
        )}),
    )
    ordering = ('username', 'date_birth', '-date_joined',)
    readonly_fields = ('date_joined',)
    list_display = ('username', 'user_img', 'date_joined', 'city')
    list_display_links = ('username',)
    save_on_top = True

    @admin.display(description='Фото пользователя', ordering='username')
    def user_img(self, user: User):
        """Функция вывода изображения, если оно есть"""
        if user.user_photo:
            return mark_safe(f'<img src="{user.user_photo.url}" width=50>')
        return 'Без фото'
