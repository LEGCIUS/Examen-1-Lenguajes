from django.contrib import admin
from .models import EvidenciaProyecto

# Panel de administración de Django para gestión interna de evidencias.
# No forma parte de los requisitos del proyecto pero Django lo incluye
# por defecto y no afecta el funcionamiento de la API.
@admin.register(EvidenciaProyecto)
class EvidenciaProyectoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'nombre_proyecto', 'responsable', 'categoria', 'fecha_registro', 'created_at']
    list_filter = ['categoria', 'fecha_registro']
    search_fields = ['titulo', 'nombre_proyecto', 'responsable']
    readonly_fields = ['url_archivo', 'nombre_archivo', 'tipo_archivo', 'tamano_archivo', 'fecha_carga', 'created_at', 'updated_at']
