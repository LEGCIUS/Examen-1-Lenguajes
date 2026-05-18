from django.db import models

# Modelo principal del sistema. Representa una evidencia digital
# asociada a un proyecto. Almacena tanto los datos descriptivos
# como la informacion del archivo subido a Cloudinary (url, nombre,
# tipo, tamano y fecha de carga).

# Categorias permitidas. Al definirlas aqui en el modelo, Django
# las valida automaticamente a nivel de base de datos y los
# serializers y filtros las heredan sin duplicar codigo.
class EvidenciaProyecto(models.Model):

    CATEGORIA_CHOICES = [
    ('documento', 'Documento'),
    ('imagen', 'Imagen'),
    ('captura_pantalla', 'Captura de pantalla'),
    ('informe', 'Informe'),
    ('presentacion', 'Presentación'),
    ('otro', 'Otro'),
]

    # Información de la evidencia
    titulo = models.CharField(max_length=255, verbose_name='Título')
    nombre_proyecto = models.CharField(max_length=255, verbose_name='Nombre del proyecto')
    responsable = models.CharField(max_length=255, verbose_name='Responsable / Autor')
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        verbose_name='Categoría'
    )
    descripcion = models.TextField(max_length=500, verbose_name='Descripción')
    fecha_registro = models.DateField(verbose_name='Fecha de registro')


    url_archivo = models.URLField(verbose_name='URL pública del archivo')
    nombre_archivo = models.CharField(max_length=255, verbose_name='Nombre original del archivo')
    tipo_archivo = models.CharField(max_length=100, verbose_name='Tipo de archivo (MIME)')
    tamano_archivo = models.PositiveIntegerField(verbose_name='Tamaño del archivo (bytes)')
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de carga')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    # Ordena las evidencias de mas reciente a mas antigua por defecto.
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Evidencia de Proyecto'
        verbose_name_plural = 'Evidencias de Proyectos'

    def __str__(self):
        return f'{self.titulo} — {self.nombre_proyecto}'
