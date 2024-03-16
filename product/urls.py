from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/v1/auth/', include('rest_framework.urls')),
]
