from django.apps import AppConfig

# Configuracion de la app de autenticacion. Se usa label='google_auth'
# para evitar choque con la app 'auth' interna de Django.
class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.auth'
    label = 'google_auth'
