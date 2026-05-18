from rest_framework import serializers
from .models import EvidenciaProyecto
from .validators import validar_archivo


# Serializer de lectura (GET). Convierte el objeto de la base de datos
# a JSON. Incluye categoria_display para mostrar el nombre legible
# de la categoria ademas del valor interno.
class EvidenciaProyectoSerializer(serializers.ModelSerializer):

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


# Clase base con las validaciones comunes de texto reutilizadas
# por el serializer de creacion y el de actualizacion.
class EvidenciaProyectoBaseSerializer(serializers.ModelSerializer):

    # Valida que el titulo no este vacio.
    def validate_titulo(self, value):
        if not value.strip():
            raise serializers.ValidationError('El título no puede estar vacío.')
        return value.strip()

    # Valida que el nombre del proyecto no este vacio.
    def validate_nombre_proyecto(self, value):
        if not value.strip():
            raise serializers.ValidationError('El nombre del proyecto no puede estar vacío.')
        return value.strip()

    # Valida que la descripcion tenga al menos 10 caracteres.
    def validate_descripcion(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                'La descripción debe tener al menos 10 caracteres.'
            )
        return value.strip()


# Serializer de creacion (POST). Incluye el campo archivo que no
# se guarda en el modelo directamente sino que se sube a Cloudinary.
# Una vez creado el objeto devuelve la representacion completa.
class EvidenciaProyectoCreateSerializer(EvidenciaProyectoBaseSerializer):

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

    # Delega la validacion del archivo al modulo validators.py.
    def validate_archivo(self, archivo):
        validar_archivo(archivo)
        return archivo

    def to_representation(self, instance):
        return EvidenciaProyectoSerializer(instance).data


# Serializer de actualizacion parcial (PATCH). Solo permite modificar
# los campos de texto, no el archivo. Este permanece en Cloudinary
# tal como fue subido originalmente.
class EvidenciaProyectoUpdateSerializer(EvidenciaProyectoBaseSerializer):

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

    def to_representation(self, instance):
        return EvidenciaProyectoSerializer(instance).data