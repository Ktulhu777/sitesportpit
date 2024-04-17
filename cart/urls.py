from django.urls import path, include
from .views import CartAPI, OrderView
from rest_framework.routers import SimpleRouter

order = SimpleRouter()
order.register('', OrderView)

urlpatterns = [
    path('cart/', CartAPI.as_view(), name='cart'),
    path('order/', include(order.urls)),
]
