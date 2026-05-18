import django_filters
from .models import EvidenciaProyecto

# Define los filtros disponibles en GET /evidencias/.
# Se usa ChoiceFilter para que la categoria aparezca como dropdown
# en Swagger en lugar de campo de texto libre, evitando errores
# al escribir un valor invalido.
class EvidenciaFilter(django_filters.FilterSet):
    categoria = django_filters.ChoiceFilter(
        choices=EvidenciaProyecto.CATEGORIA_CHOICES
    )

    class Meta:
        model = EvidenciaProyecto
        fields = ['categoria', 'nombre_proyecto']