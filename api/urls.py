from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


# Router principal de la API. Conecta todas las rutas de las apps
# y agrega los endpoints de documentacion Swagger y el health check.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('api.auth.urls')),
    path('evidencias/', include('api.evidencias.urls')),
    path('health/', include('api.health')),
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
