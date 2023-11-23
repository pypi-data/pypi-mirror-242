from typing import Union

import django_filters
from django.db.models import QuerySet, Q
from rest_framework.exceptions import ValidationError

from modules.appeals_pos.models import Appeal
from modules.appeals_pos.models.subcategory import Subcategory
from modules.appeals_pos.models.appeal import AppealState


class AppealFilter(django_filters.FilterSet):
    subcategories = django_filters.CharFilter(method="filter_subcategories")
    categories = django_filters.CharFilter(method="filter_categories")
    status = django_filters.CharFilter(method="filter_state")
    locality = django_filters.NumberFilter(method="filter_locality")

    def filter_subcategories(
        self, queryset: Union[QuerySet, Appeal], name: str, value: str
    ) -> Union[QuerySet, Appeal]:
        if "," not in value:
            return queryset.filter(subcategory_id=int(value))

        try:
            subcategories_string_list = value.split(",")
            subcategories_ids = map(
                lambda subcategory_str: int(subcategory_str), subcategories_string_list
            )
            return queryset.filter(subcategory_id__in=subcategories_ids)

        except (ValueError, TypeError):
            raise ValidationError("Неккоректный фильтр подкатегорий")

    def filter_categories(self, queryset: Union[QuerySet, Appeal], name: str, value: str) -> Union[QuerySet, Appeal]:
        if "," not in value:
            return queryset.filter(
                subcategory_id__in=Subcategory.objects.filter(category_id=value).values_list("id", flat=True)
            )

        try:
            categories_string_list = value.split(",")
            categories_ids = map(
                lambda category_str: int(category_str), categories_string_list
            )
            return queryset.filter(subcategory_id__in=Subcategory.objects.filter(
                category_id__in=categories_ids).values_list("id", flat=True)
            )

        except (ValueError, TypeError):
            raise ValidationError("Неккоректный фильтр Категорий")

    def filter_state(
        self, queryset: Union[QuerySet, Appeal], name: str, value: str
    ) -> Union[QuerySet, Appeal]:
        if "," not in value:
            return queryset.filter(status=value.upper())
        query = Q()
        status_string_list = value.split(",")
        for status in status_string_list:
            if status.upper() in AppealState.RESOLVER.keys():
                query |= Q(status=status)
            else:
                raise ValidationError("Неккоректный фильтр статуса")
        return queryset.filter(query)

    def filter_locality(
        self, queryset: Union[QuerySet, Appeal], name: str, value: int
    ) -> Union[QuerySet, Appeal]:
        return queryset.filter(locality_id=value)
