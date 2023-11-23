import django_filters

from modules.integration.utils.filter import NumberInFilter
from modules.voting.models import Vote


class VoteFilter(django_filters.FilterSet):
    is_opened = django_filters.BooleanFilter()
    category = NumberInFilter()
    locality = NumberInFilter()

    class Meta:
        model = Vote
        fields = []


