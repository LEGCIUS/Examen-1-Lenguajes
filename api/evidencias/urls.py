from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvidenciaProyectoViewSet


# El router de DRF genera automaticamente todas las rutas del CRUD
# a partir del ViewSet: GET /evidencias/, POST /evidencias/,
# GET /evidencias/{id}/, PATCH /evidencias/{id}/, DELETE /evidencias/{id}/
router = DefaultRouter()


# Registra el ViewSet en la raiz del router (sin prefijo adicional
# porque la url base /evidencias/ ya esta definida en api/urls.py).
router.register(r'', EvidenciaProyectoViewSet, basename='evidencia')

urlpatterns = [
    path('', include(router.urls)),
]
