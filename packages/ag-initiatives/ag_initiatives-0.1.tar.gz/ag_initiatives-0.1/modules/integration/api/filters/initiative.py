import django_filters

from modules.initiatives.models import Initiative
from modules.integration.utils.filter import NumberInFilter, CharInFilter


class InitiativeFilter(django_filters.FilterSet):
    state = CharInFilter()
    category = NumberInFilter()
    locality = NumberInFilter()

    class Meta:
        model = Initiative
        fields = []
