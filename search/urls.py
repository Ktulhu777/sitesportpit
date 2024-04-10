from django.urls import path

from search.views import SearchProduct

urlpatterns = [
    path('product/<str:query>/', SearchProduct.as_view()),
]


