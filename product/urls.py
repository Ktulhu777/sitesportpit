from django.urls import path
from . import views

urlpatterns = [
    path('like/', views.LikeProductViews.as_view({'post': 'create'})),
    path('like/<int:pk>/', views.LikeProductViews.as_view({'delete': 'destroy'})),
    path('search/', views.SearchProduct.as_view()),
    path('product-list/', views.ProductAllView.as_view()),
    path('product-list/<int:pk>/', views.ProductDetailView.as_view()),
    path('product-list/<slug:product_slug>/', views.ProductDetailView.as_view()),
    path('category/', views.CategoryProductView.as_view()),
    path('category/<slug:slug>/', views.CategoryProductView.as_view()),
    path('order-add', views.OrderView.as_view()),
]
