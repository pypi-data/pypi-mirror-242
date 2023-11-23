import django_filters

from modules.core.models import Locality
from modules.initiatives.models import (
    InitiativeCategory,
    Initiative,
    InitiativeState,
)


class InitiativeFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method='filter_categories')
    state = django_filters.MultipleChoiceFilter(
        choices=[(k, v) for k, v in InitiativeState.CHOICES],
    )
    states = django_filters.CharFilter(method='filter_states')
    locality = django_filters.ModelMultipleChoiceFilter(queryset=Locality.objects.all())

    class Meta:
        model = Initiative
        fields = [
            "category",
            "locality",
            "state",
            "states",
        ]

    def filter_categories(self, queryset, _, value):
        return queryset.filter(category__in=value.split(','))

    def filter_states(self, queryset, _, value):
        return queryset.filter(state__in=value.split(','))
