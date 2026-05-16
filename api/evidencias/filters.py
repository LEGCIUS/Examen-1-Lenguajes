import django_filters
from .models import EvidenciaProyecto


class EvidenciaFilter(django_filters.FilterSet):
    categoria = django_filters.ChoiceFilter(
        choices=EvidenciaProyecto.CATEGORIA_CHOICES
    )

    class Meta:
        model = EvidenciaProyecto
        fields = ['categoria', 'nombre_proyecto']