from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvidenciaProyectoViewSet

router = DefaultRouter()
router.register(r'', EvidenciaProyectoViewSet, basename='evidencia')

urlpatterns = [
    path('', include(router.urls)),
]
