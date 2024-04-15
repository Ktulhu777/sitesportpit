from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home, name='home'),
    path('v1/search/', views.SearchProduct.as_view()),
    path('v1/product-list/', views.ProductAllView.as_view()),
    path('v1/product-list/<int:pk>/', views.IDProduct.as_view()),
    path('v1/product-list/<int:pk>/', views.ProductDetailView.as_view()),
    path('v1/product-list/<slug:product_slug>/', views.ProductDetailView.as_view()),
    path('v1/category/', views.CategoryProductView.as_view()),
    path('v1/category/<slug:slug>/', views.CategoryProductView.as_view()),
]
