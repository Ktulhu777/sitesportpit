from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path("users/", include("djoser.urls")),
    path("user/", include("djoser.urls.jwt")),
    path('account/activate/<uid>/<token>', views.ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path('api-auth/', include('rest_framework.urls')),  # => in end_url /login/ or  /logout/
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # give jwt-token - access and refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # give access token by refresh
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # unknown
]
