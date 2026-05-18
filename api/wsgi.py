import os
from django.core.wsgi import get_wsgi_application


# Punto de entrada WSGI para el servidor en produccion (gunicorn).
# Define que archivo de settings usar por defecto. En produccion
# Railway usa el Procfile que llama a gunicorn con este modulo.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
application = get_wsgi_application()
