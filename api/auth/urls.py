from django.urls import path
from . import views


# Ruta de autenticacion. POST /auth/google/ recibe el token de Google
# y devuelve los tokens JWT.
urlpatterns = [
    path('google/', views.google_login, name='auth-google'),
]
