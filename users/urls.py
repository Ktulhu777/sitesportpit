from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [  # ↓ http://127.0.0.1:8000/user/registration/ ↓
    path('registration/', views.UserViewSet.as_view({'post': 'create'})),
    # => registration user, form: username, password
    path('api-auth/', include('rest_framework.urls')),  # => in end_url /login/ or  /logout/
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # give jwt-token - access and refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # give access token by refresh
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # unknown
    path('profile/<str:username>/', views.ProfileView.as_view())

]
