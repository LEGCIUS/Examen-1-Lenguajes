from .base import *


# Configuracion para desarrollo local. Extiende base.py con
# DEBUG activado para ver errores detallados en pantalla.
DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
