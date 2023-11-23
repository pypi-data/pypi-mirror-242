import django_filters
from django.db.models import Q
from pydantic import ValidationError

from modules.core.models import LocalityType, Locality
from modules.core.models.locality import LocalityCategory


class VotingFilter(django_filters.FilterSet):
    """FilterSet для Голосовани:
    state -> str - method filter_state - можно перечислять через запятую
    """

    state = django_filters.CharFilter(method='filter_state')
    department = django_filters.NumberFilter(method="filter_department")
    locality = django_filters.ModelMultipleChoiceFilter(queryset=Locality.objects.all())
    category = django_filters.NumberFilter(method='filter_category')


    def filter_state(self, queryset, name, value):
        if "," not in value and ", " not in value:
            return queryset.filter(state=value)

        try:
            state_list = value.split(",")
            return queryset.filter(state__in=state_list)
        except (ValueError, TypeError):
            raise ValidationError("Некорректный фильтр статуса")


    def filter_department(self, queryset, name, value: int):
        return queryset.filter(department__id=value)

    def filter_category(self, queryset, name, value: int):
        return queryset.filter(category_id=value)
