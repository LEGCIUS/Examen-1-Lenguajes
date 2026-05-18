# API Evidencias Digitales

API REST para gestión de evidencias digitales asociadas a proyectos académicos o profesionales.

## Descripción

Permite a usuarios autenticados registrar, consultar, actualizar y eliminar evidencias digitales (documentos, imágenes, capturas, informes) asociadas a proyectos. Los archivos se almacenan en Cloudinary y se acceden mediante URL pública CDN.

## Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Framework | Django 4.2 + Django REST Framework |
| Autenticación | Google SSO + JWT (SimpleJWT) |
| Almacenamiento archivos | Cloudinary |
| Base de datos | SQLite |
| Documentación API | drf-spectacular (Swagger/OpenAPI) |
| Pipeline CI | GitHub Actions |
| Despliegue | Railway / Render |

## Instalación local

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd evidencias_proyecto
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Nota:** Todos los comandos siguientes deben ejecutarse con el entorno virtual activo. 
> Verifica que tu terminal muestre `(venv)` al inicio antes de ejecutar cualquier comando.

# Activar el entorno virtual
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales reales
```

### 4. Crear la base de datos y superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Ejecutar el servidor

```bash
{python manage.py runserver}
```

La API estará disponible en `http://localhost:8000`
La documentación Swagger en `http://localhost:8000/api/docs/`

## Variables de entorno requeridas

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `True` en desarrollo, `False` en producción |
| `GOOGLE_CLIENT_ID` | Client ID de Google OAuth 2.0 |
| `CLOUDINARY_CLOUD_NAME` | Nombre del cloud en Cloudinary |
| `CLOUDINARY_API_KEY` | API Key de Cloudinary |
| `CLOUDINARY_API_SECRET` | API Secret de Cloudinary |

## Endpoints principales

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/auth/google/` | Login con Google → retorna JWT | No |
| GET | `/health/` | Verifica que la API esté activa | No |
| GET | `/evidencias/` | Lista evidencias (paginada, con filtros) | JWT |
| POST | `/evidencias/` | Crea evidencia con archivo | JWT |
| GET | `/evidencias/{id}/` | Detalle de una evidencia | JWT |
| PATCH | `/evidencias/{id}/` | Actualiza datos de evidencia | JWT |
| DELETE | `/evidencias/{id}/` | Elimina evidencia | JWT |
| GET | `/api/docs/` | Documentación Swagger | No |

### Parámetros de consulta en GET /evidencias/

| Parámetro | Descripción | Ejemplo |
|---|---|---|
| `categoria` | Filtrar por categoría | `?categoria=imagen` |
| `nombre_proyecto` | Filtrar por proyecto | `?nombre_proyecto=ProyectoX` |
| `search` | Buscar en título y responsable | `?search=informe` |
| `ordering` | Ordenar resultados | `?ordering=-created_at` |
| `page` | Página de resultados | `?page=2` |

## Arquitectura

```
evidencias_proyecto/
├── api/
│   ├── auth/              # App autenticación (Google SSO + JWT)
│   ├── evidencias/        # App principal (CRUD evidencias)
│   │   ├── models.py      # Modelo EvidenciaProyecto
│   │   ├── serializers.py # Validación entrada/salida
│   │   ├── views.py       # ViewSet con lógica de negocio
│   │   ├── validators.py  # Validación de archivos
│   │   └── urls.py        # Rutas de la app
│   ├── services/
│   │   └── cloudinary_service.py  # Carga de archivos a CDN
│   └── urls.py            # Router global
├── settings/
│   ├── base.py            # Configuración común
│   ├── dev.py             # Configuración desarrollo
│   └── prod.py            # Configuración producción
├── .github/workflows/     # Pipeline CI
├── requirements.txt
└── manage.py
```

## Generar token JWT para pruebas locales

Como alternativa a Google SSO, puedes generar un token de prueba desde el shell de Django:

```bash
python manage.py shell
```

```pythonhttps://res.cloudinary.com/dm8tazlaf/image/upload/v1779062249/evidencias/Captura_de_pantalla_2026-05-13_201436_e2kd9d.png
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

user = User.objects.create_user(username='test@test.com', password='test123')
refresh = RefreshToken.for_user(user)
print(str(refresh.access_token))
```


Copia el token generado y pégalo en el botón **Authorize** de Swagger para probar los endpoints protegidos.

> **Nota:** Asegúrate de tener el entorno virtual activo `(venv)` antes de ejecutar estos comandos.

> **Nota 2:** En caso tal de que queramos volver a conseguir el token usando este metodo anterior, muy probablemente nos vaya a dar error por como esta puesto el codigo ya que estamos creado variables y si lo volvemos a ejecutar va a dar error por que ya existe

Solucion:

```python
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

user, created = User.objects.get_or_create(username='test@test.com')
if created:
    user.set_password('test123')
    user.save()

refresh = RefreshToken.for_user(user)
print(str(refresh.access_token))
```


## Despliegue

URL pública: **https://examen-1-lenguajes-production.up.railway.app/api/docs/**

### Desplegar en Railway

1. Crear cuenta en [railway.app](https://railway.app)
2. Conectar el repositorio de GitHub
3. Agregar las variables de entorno en el panel de Railway
4. Railway detecta automáticamente el proyecto Django

## Problemas encontrados y soluciones aplicadas

- Python no estaba instalado — se instaló desde python.org marcando "Add to PATH"
- El pipeline de CI estaba configurado para la rama `main` pero el proyecto usa `master` — se corrigió el archivo ci.yml
- Railway usaba el puerto 8080 en lugar de 8000 — se actualizó el Target Port en Railway
- El deployment crasheó por falta de variables de entorno — se agregaron en el panel de Railway

