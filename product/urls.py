from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'review', views.ReviewProductChangesView)

urlpatterns = [
    path('like/', views.LikeProductViews.as_view({'post': 'create'})),
    path('like/<int:pk>/', views.LikeProductViews.as_view({'delete': 'destroy'})),
    path('product-list/', views.ProductAllView.as_view()),
    path('product-list/<int:pk>/', views.ProductDetailView.as_view()),
    path('product-list/<slug:product_slug>/', views.ProductDetailView.as_view()),
    path('v1/review/<slug:product_slug>/', views.ReviewProductView.as_view()),
    path('v1/changes/', include(router.urls)),
    path('category/', views.CategoryProductView.as_view()),
    path('category/<slug:slug>/', views.CategoryProductView.as_view()),
]
