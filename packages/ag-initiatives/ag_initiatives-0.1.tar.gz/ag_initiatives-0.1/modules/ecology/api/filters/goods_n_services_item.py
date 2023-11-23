import django_filters
from django.db.models import Q

from modules.ecology.models import GoodsNServicesItem, GoodsNServicesItemCategory


class GoodsNServicesItemFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=GoodsNServicesItemCategory.objects.all()
    )
    locality = django_filters.CharFilter(
        field_name="display_localities",
        method="filter_display_localities"
    )

    def filter_display_localities(self, queryset, name, value):
        query = Q(display_localities__id=value) | Q(locality__id=value)
        queryset = queryset.filter(query).distinct()

        return queryset

    class Meta:
        model = GoodsNServicesItem
        fields = [
            "category",
            "locality",
        ]
