from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.SearchProduct.as_view()),
    path('api/v1/product-list/', views.ProductView.as_view()),
    path('api/v1/product-list/<slug:slug>/', views.ProductView.as_view()),
    path('api/v1/category/', views.CategoryProductView.as_view()),
    path('api/v1/category/<slug:slug>/', views.CategoryProductView.as_view()),
]
