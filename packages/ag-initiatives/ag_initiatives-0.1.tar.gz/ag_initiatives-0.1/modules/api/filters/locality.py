from django_filters import rest_framework as filters

from modules.core.models import Locality


class LocalityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Locality
        fields = ("name",)
