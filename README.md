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
python manage.py runserver
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

## Despliegue

URL pública: **[por completar]**

### Desplegar en Railway

1. Crear cuenta en [railway.app](https://railway.app)
2. Conectar el repositorio de GitHub
3. Agregar las variables de entorno en el panel de Railway
4. Railway detecta automáticamente el proyecto Django

## Problemas encontrados y soluciones

_Por completar durante el desarrollo_

---

Proyecto desarrollado como actividad académica — Gestión de Evidencias Digitales.
