from django.urls import path
from . import views

urlpatterns = [
    path('telegram/<int:telegram_id>/', views.TelegramViews.as_view()),
    path('<int:telegram>/', views.func)
]
