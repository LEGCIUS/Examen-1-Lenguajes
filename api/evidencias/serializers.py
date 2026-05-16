from rest_framework import serializers
from .models import EvidenciaProyecto
from .validators import validar_archivo


class EvidenciaProyectoSerializer(serializers.ModelSerializer):
    """Serializer para lectura (GET) de evidencias."""

    categoria_display = serializers.CharField(
        source='get_categoria_display',
        read_only=True
    )

    class Meta:
        model = EvidenciaProyecto
        fields = [
            'id',
            'titulo',
            'nombre_proyecto',
            'responsable',
            'categoria',
            'categoria_display',
            'descripcion',
            'fecha_registro',
            'url_archivo',
            'nombre_archivo',
            'tipo_archivo',
            'tamano_archivo',
            'fecha_carga',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'url_archivo', 'nombre_archivo', 'tipo_archivo',
            'tamano_archivo', 'fecha_carga', 'created_at', 'updated_at',
        ]


class EvidenciaProyectoCreateSerializer(serializers.ModelSerializer):
    """Serializer para creación de evidencias (incluye el campo archivo)."""

    archivo = serializers.FileField(write_only=True)

    class Meta:
        model = EvidenciaProyecto
        fields = [
            'titulo',
            'nombre_proyecto',
            'responsable',
            'categoria',
            'descripcion',
            'fecha_registro',
            'archivo',
        ]

    def validate_titulo(self, value):
        if not value.strip():
            raise serializers.ValidationError('El título no puede estar vacío.')
        return value.strip()

    def validate_nombre_proyecto(self, value):
        if not value.strip():
            raise serializers.ValidationError('El nombre del proyecto no puede estar vacío.')
        return value.strip()

    def validate_descripcion(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                'La descripción debe tener al menos 10 caracteres.'
            )
        return value.strip()

    def validate_archivo(self, archivo):
        validar_archivo(archivo)
        return archivo

    def to_representation(self, instance):
        """Al crear, devuelve la representación completa del objeto."""
        return EvidenciaProyectoSerializer(instance).data


class EvidenciaProyectoUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualización parcial (PATCH) de evidencias."""

    class Meta:
        model = EvidenciaProyecto
        fields = [
            'titulo',
            'nombre_proyecto',
            'responsable',
            'categoria',
            'descripcion',
            'fecha_registro',
        ]

    def validate_titulo(self, value):
        if not value.strip():
            raise serializers.ValidationError('El título no puede estar vacío.')
        return value.strip()

    def validate_nombre_proyecto(self, value):
        if not value.strip():
            raise serializers.ValidationError('El nombre del proyecto no puede estar vacío.')
        return value.strip()

    def to_representation(self, instance):
        return EvidenciaProyectoSerializer(instance).data
