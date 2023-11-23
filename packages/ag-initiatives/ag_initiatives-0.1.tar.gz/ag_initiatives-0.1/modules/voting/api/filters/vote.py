from typing import Union

import django_filters
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from modules.core.models import Category
from modules.voting.models import Vote, VoteState


class VoteFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())
    state = django_filters.CharFilter(method="filter_state")
    department = django_filters.NumberFilter(method="filter_department")
    # is_opened = django_filters.BooleanFilter(
    #     method='filter__is_opened'
    # )

    class Meta:
        model = Vote
        fields = [
            "locality",
            "category",
            "is_opened",
            "state",
            "department"
        ]

    def filter_state(
        self, queryset: Union[QuerySet, Vote], name: str, value: str
    ) -> Union[QuerySet, Vote]:
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

    # def filter__is_opened(self, queryset, name, value):
    #     original_queryset = queryset
    #
    #     queryset = queryset.filter(is_opened=value)
    #
    #     locality_id = self.data.get('locality', None)
    #     if locality_id is not None and queryset.filter(locality__pk=locality_id).count() == 0 and value is True:
    #         queryset = original_queryset
    #
    #     return queryset


class VoteStatsFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Vote
        fields = [
            "locality",
            "category",
        ]
