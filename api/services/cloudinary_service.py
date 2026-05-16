import cloudinary.uploader
from rest_framework.exceptions import ValidationError


def subir_archivo(archivo, carpeta='evidencias'):
    """
    Sube un archivo a Cloudinary y retorna la información del resultado.

    Args:
        archivo: InMemoryUploadedFile o TemporaryUploadedFile de Django
        carpeta: carpeta en Cloudinary donde se almacenará

    Returns:
        dict con url, nombre_archivo, tipo_archivo, tamano_archivo
    """
    try:
        # Determinar el tipo de recurso según el content_type
        resource_type = 'raw'
        if archivo.content_type.startswith('image/'):
            resource_type = 'image'

        resultado = cloudinary.uploader.upload(
            archivo,
            folder=carpeta,
            resource_type=resource_type,
            use_filename=True,
            unique_filename=True,
        )

        return {
            'url_archivo': resultado.get('secure_url'),
            'nombre_archivo': archivo.name,
            'tipo_archivo': archivo.content_type,
            'tamano_archivo': archivo.size,
        }

    except Exception as e:
        raise ValidationError(
            f'Error al subir el archivo a Cloudinary: {str(e)}'
        )


def eliminar_archivo(public_id):
    """
    Elimina un archivo de Cloudinary por su public_id.
    No lanza error si el archivo no existe.
    """
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass
