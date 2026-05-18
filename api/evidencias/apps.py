from django.apps import AppConfig

# Configuracion de la app principal del proyecto.
# Contiene el CRUD completo de evidencias digitales:
# modelo, serializers, validaciones, filtros y vistas.
class EvidenciasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.evidencias'
