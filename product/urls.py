from django.urls import path
from . import views

urlpatterns = [
    path('v1/like/', views.LikeProductViews.as_view({'post': 'create'})),
    path('v1/like/<int:pk>/', views.LikeProductViews.as_view({'delete': 'destroy'})),
    path('v1/search/', views.SearchProduct.as_view()),
    path('v1/product-list/', views.ProductAllView.as_view()),
    path('v1/product-list/<int:pk>/', views.ProductDetailView.as_view()),
    path('v1/product-list/<slug:product_slug>/', views.ProductDetailView.as_view()),
    path('v1/category/', views.CategoryProductView.as_view()),
    path('v1/category/<slug:slug>/', views.CategoryProductView.as_view()),
    path('v1/order-add', views.OrderView.as_view()),
]
