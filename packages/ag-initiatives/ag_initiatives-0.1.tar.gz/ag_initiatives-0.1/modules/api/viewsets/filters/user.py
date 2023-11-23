from typing import Union

import django_filters as filters
from django.db.models import QuerySet, Q
from rest_framework.exceptions import ValidationError

from modules.core.models import User


def get_search_filter_by_fio(FIO: str):
    FIO = FIO.split(" ")
    if len(FIO) == 1:
        return Q(last_name__icontains=FIO[0]) | Q(
            first_name__icontains=FIO[0]
        )
    else:
        return Q(
            last_name__icontains=FIO[0], first_name__icontains=FIO[1]
        ) | Q(first_name__icontains=FIO[0], last_name__icontains=FIO[1])


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_fio")
    roles = filters.CharFilter(method="filter_roles")
    department = filters.NumberFilter(method="filter_department")
    status = filters.CharFilter(method="filter_status")

    def search_fio(
            self, queryset: Union[QuerySet, User], name: str, value: str
    ) -> Union[QuerySet, User]:
        try:
            return queryset.filter(get_search_filter_by_fio(value))
        except (ValueError, TypeError):
            raise ValidationError("Неккоректный фильтро по ФИО")

    def filter_roles(
            self, queryset: Union[QuerySet, User], name: str, value: str
    ) -> Union[QuerySet, User]:
        if "," not in value and ", " not in value:
            return queryset.filter(roles__icontains=value)

        try:
            roles_list = value.split(",")
            query = Q()
            for role in roles_list:
                query = query | Q(roles__icontains=role)
            return queryset.filter(query)
        except (ValueError, TypeError):
            raise ValidationError("Неккоректный фильтр ролей")

    def filter_department(
            self, queryset: Union[QuerySet, User], name: str, value: int
    ) -> Union[QuerySet, User]:
        operator_filter = Q(sub_permissions__operator_permissions__department__id=value)
        admin_lko_filter = Q(sub_permissions__admin_lko_permissions__department__id=value)
        curator_filter = Q(sub_permissions__curator_permissions__department__id=value)
        return queryset.filter(operator_filter | admin_lko_filter | curator_filter)

    def filter_status(
            self, queryset: Union[QuerySet, User], name: str, value: int
    ) -> Union[QuerySet, User]:
        if "," not in value and ", " not in value:
            return queryset.filter(sub_permissions__status=value)

        try:
            status_list = value.split(",")
            return queryset.filter(sub_permissions__status__in=status_list)
        except (ValueError, TypeError):
            raise ValidationError("Неккоректный фильтр статуса")
