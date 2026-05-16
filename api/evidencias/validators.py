from django.core.exceptions import ValidationError

TIPOS_PERMITIDOS = ['image/jpeg', 'image/png', 'application/pdf']
TAMANO_MAXIMO_MB = 5
TAMANO_MAXIMO_BYTES = TAMANO_MAXIMO_MB * 1024 * 1024  # 5 MB


def validar_archivo(archivo):
    """
    Valida que el archivo:
    - Exista en la solicitud
    - Sea de un tipo permitido (JPEG, PNG, PDF)
    - No supere el tamaño máximo (5 MB)
    """
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
