from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
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
        parameters=[
            OpenApiParameter('categoria', description='Filtrar por categoría', required=False),
            OpenApiParameter('nombre_proyecto', description='Filtrar por nombre de proyecto', required=False),
            OpenApiParameter('search', description='Buscar en título y responsable', required=False),
            OpenApiParameter('ordering', description='Ordenar por campo (ej: -created_at, titulo)', required=False),
        ],
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
class EvidenciaProyectoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de evidencias digitales de proyectos.
    Todos los endpoints requieren autenticación JWT.
    """
    queryset = EvidenciaProyecto.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    # Filtros, búsqueda y ordenamiento
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'nombre_proyecto']
    search_fields = ['titulo', 'responsable']
    ordering_fields = ['created_at', 'fecha_registro', 'titulo', 'nombre_proyecto']
    ordering = ['-created_at']

    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return EvidenciaProyectoCreateSerializer
        if self.action == 'partial_update':
            return EvidenciaProyectoUpdateSerializer
        return EvidenciaProyectoSerializer

    def create(self, request, *args, **kwargs):
        """
        POST /evidencias
        Recibe multipart/form-data con los datos y el archivo.
        Sube el archivo a Cloudinary y guarda la URL en la BD.
        """
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

    def partial_update(self, request, *args, **kwargs):
        """PATCH /evidencias/{id} — actualiza campos de texto, no el archivo."""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    # Deshabilitar PUT (solo PATCH permitido)
    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial'):
            return Response(
                {'error': 'Usar PATCH para actualizar. PUT no está habilitado.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)
