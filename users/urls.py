from django.urls import path, include
from . import views

urlpatterns = [
    path('api/v1/auth/', include('rest_framework.urls')),
]
