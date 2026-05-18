from .filters import EvidenciaFilter
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import EvidenciaProyecto
from .serializers import (
    EvidenciaProyectoSerializer,
    EvidenciaProyectoCreateSerializer,
    EvidenciaProyectoUpdateSerializer,
)
from api.services.cloudinary_service import subir_archivo


@extend_schema_view(
    list=extend_schema(
        summary='Listar evidencias',
        description='Retorna lista paginada de evidencias. Soporta filtros por categoría y proyecto, búsqueda por título, y ordenamiento.',
        tags=['Evidencias'],
    ),
    create=extend_schema(
        summary='Crear evidencia',
        description='Crea una nueva evidencia con archivo adjunto. Usar Content-Type: multipart/form-data.',
        tags=['Evidencias'],
    ),
    retrieve=extend_schema(
        summary='Obtener evidencia',
        description='Retorna el detalle de una evidencia por ID.',
        tags=['Evidencias'],
    ),
    partial_update=extend_schema(
        summary='Actualizar evidencia',
        description='Actualiza uno o más campos de una evidencia. No actualiza el archivo.',
        tags=['Evidencias'],
    ),
    destroy=extend_schema(
        summary='Eliminar evidencia',
        description='Elimina una evidencia de la base de datos.',
        tags=['Evidencias'],
    ),
)


# ViewSet principal del sistema. Maneja todas las operaciones CRUD
# de evidencias. Todos los endpoints requieren autenticacion JWT.
# Se usa ModelViewSet como base para aprovechar las operaciones
# estandar de DRF y sobreescribir solo lo que necesita logica extra.

# Configuracion del ViewSet: permisos, parsers y filtros.
# MultiPartParser permite recibir archivos, JSONParser permite
# recibir datos en formato JSON.
class EvidenciaProyectoViewSet(viewsets.ModelViewSet):

    queryset = EvidenciaProyecto.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EvidenciaFilter
    search_fields = ['titulo', 'responsable']
    ordering_fields = ['created_at', 'fecha_registro', 'titulo', 'nombre_proyecto']
    ordering = ['-created_at']

    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']



# Selecciona el serializer segun la operacion:
# - Crear: incluye el campo archivo para subir a Cloudinary
# - Actualizar: solo campos de texto, sin archivo
# - Resto: serializer de lectura completo
    def get_serializer_class(self):
        if self.action == 'create':
            return EvidenciaProyectoCreateSerializer
        if self.action == 'partial_update':
            return EvidenciaProyectoUpdateSerializer
        return EvidenciaProyectoSerializer
    


# Creacion de evidencia. El flujo es:
# 1. Valida los datos del formulario con el serializer
# 2. Extrae el archivo del request
# 3. Sube el archivo a Cloudinary y obtiene la URL publica
# 4. Guarda la evidencia en la base de datos con la URL del archivo
# 5. Devuelve la evidencia completa con codigo 201
    def create(self, request, *args, **kwargs):
  
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        archivo = serializer.validated_data.pop('archivo')

        # Subir archivo a Cloudinary
        info_archivo = subir_archivo(archivo)

        # Guardar evidencia con info del archivo
        evidencia = EvidenciaProyecto.objects.create(
            **serializer.validated_data,
            **info_archivo,
        )

        output = EvidenciaProyectoSerializer(evidencia)
        return Response(output.data, status=status.HTTP_201_CREATED)


# Actualizacion parcial (PATCH). Solo actualiza los campos de texto.
# El archivo no se puede cambiar una vez subido a Cloudinary.
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    


    # PUT esta deshabilitado. Solo se permite PATCH para actualizaciones
    # parciales, evitando que se sobreescriban campos obligatorios.
    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial'):
            return Response(
                {'error': 'Usar PATCH para actualizar. PUT no está habilitado.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)
