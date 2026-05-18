from .base import *

# Configuracion para produccion (Railway). Extiende base.py con
# DEBUG desactivado y HTTPS forzado mediante el header de Railway.
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
