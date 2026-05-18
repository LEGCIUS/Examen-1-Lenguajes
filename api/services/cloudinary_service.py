import cloudinary.uploader
from rest_framework.exceptions import ValidationError

# Sube un archivo a Cloudinary (CDN externo) y devuelve sus metadatos:
# url pública, nombre original, tipo y tamaño. La API nunca guarda
# archivos en el servidor local.
def subir_archivo(archivo, carpeta='evidencias'):
    
    try:
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


# Elimina un archivo de Cloudinary por su public_id. No lanza error
# si el archivo no existe para no interrumpir el borrado de la evidencia.
def eliminar_archivo(public_id):

    try:
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass
