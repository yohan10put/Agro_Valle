"""
URL configuration for Agro_Valle project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_health(request):
    return Response({
        'status': 'online',
        'project': 'Agro_Valle API',
        'database': 'PostgreSQL (agrovalle)',
        'auth': 'JWT (SimpleJWT)'
    })

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Health Check
    path('api/', api_health, name='api_health'),

    # Autenticación JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
