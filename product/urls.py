from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/v1/product-list/', views.ProductViewSet.as_view({'get': 'list'})),
    path('api/v1/product-list/<slug:slug>/', views.ProductViewSet.as_view({'get': 'list'})),
    # что то

]
