from django.core.exceptions import ValidationError
# Tipos de archivo permitidos y tamaño maximo (5 MB).
# Centralizar estos valores aqui facilita cambiarlos sin tocar
# la logica de validacio

TIPOS_PERMITIDOS = ['image/jpeg', 'image/png', 'application/pdf']
TAMANO_MAXIMO_MB = 5
TAMANO_MAXIMO_BYTES = TAMANO_MAXIMO_MB * 1024 * 1024 


# Valida que el archivo exista, sea de un tipo permitido y no supere
# el tamaño maximo. Se llama desde el serializer de creacion antes
# de subir el archivo a Cloudinary.
def validar_archivo(archivo):
   
    if not archivo:
        raise ValidationError('El archivo es requerido.')

    content_type = getattr(archivo, 'content_type', None)
    if content_type not in TIPOS_PERMITIDOS:
        raise ValidationError(
            f'Tipo de archivo no permitido: "{content_type}". '
            f'Se aceptan: {", ".join(TIPOS_PERMITIDOS)}.'
        )

    if archivo.size > TAMANO_MAXIMO_BYTES:
        mb_actual = round(archivo.size / (1024 * 1024), 2)
        raise ValidationError(
            f'El archivo pesa {mb_actual} MB. El máximo permitido es {TAMANO_MAXIMO_MB} MB.'
        )

    return archivo
