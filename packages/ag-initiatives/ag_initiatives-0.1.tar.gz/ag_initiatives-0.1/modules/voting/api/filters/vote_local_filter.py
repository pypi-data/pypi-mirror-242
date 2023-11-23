from typing import Union

import django_filters
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from modules.core.models import Category
from modules.voting.models import VoteLocal, VoteState


class VoteLocalFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())
    state = django_filters.CharFilter(method="filter_state")
    department = django_filters.NumberFilter(method="filter_department")

    class Meta:
        model = VoteLocal
        fields = [
            "locality",
            "municipal_formation",
            "category",
            "is_opened",
            "state",
            "department"
        ]

    def filter_state(
        self, queryset: Union[QuerySet, VoteLocal], name: str, value: str
    ) -> Union[QuerySet, VoteLocal]:
        value = value.upper()
        if "," not in value:
            return queryset.filter(state=value)

        try:
            states_list = value.split(",")
            return queryset.filter(state__in=states_list)

        except (ValueError, TypeError):
            raise ValidationError("Неккоректный фильтр подкатегорий")

    def filter_department(self, queryset, name, value: int):
        return queryset.filter(department__id=value)


class LocalStatsFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = VoteLocal
        fields = [
            "locality",
            "category",
        ]
