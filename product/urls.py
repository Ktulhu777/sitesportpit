from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'review', views.ReviewProductChangesView)

like = routers.SimpleRouter()
like.register('', views.LikeProductViews)

urlpatterns = [
    path('like/', include(like.urls)),
    path('product-list/', views.ProductAllView.as_view()),
    path('product-list/<slug:product_slug>/', views.ProductDetailView.as_view()),
    path('review/<slug:product_slug>/', views.ReviewProductView.as_view()),
    path('changes/', include(router.urls)),
    path('category/', views.CategoryProductView.as_view()),
    path('category/<slug:slug>/', views.CategoryProductView.as_view()),
]
