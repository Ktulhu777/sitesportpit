from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/v1/', include('product.urls')),
    path('', include('users.urls')),
    # path('api/search/', include('search.urls')),
    path('api/v1/', include('cart.urls')),
    path("api/__debug__/", include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
