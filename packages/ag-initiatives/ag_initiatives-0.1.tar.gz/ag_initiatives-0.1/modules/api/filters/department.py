from typing import Union

from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import QuerySet, Q
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from modules.core.models import Department, DepartmentStatus


class DepartmentFilter(filters.FilterSet):
    search_name = filters.CharFilter(method="filter_search_name")
    status = filters.CharFilter(method="filter_status")

    def filter_search_name(
        self, queryset: Union[QuerySet, Department], name: str, value: str
    ) -> Union[QuerySet, Department]:
        print(80 * "*")
        print(80 * "*")
        print(80 * "*")
        print(80 * "*")
        print(80 * "*")

        return queryset.filter(name__icontains=value)

    def filter_status(
        self, queryset: Union[QuerySet, Department], name: str, value: str
    ) -> Union[QuerySet, Department]:
        if value.upper() not in DepartmentStatus.RESOLVER.keys():
            raise ValidationError("Некорректный статус организации")

        return queryset.filter(status=value.upper())

    class Meta:
        model = Department
        fields = ["search_name", "status"]


class CommonDepartmentFilter(DepartmentFilter):
    """Реализация простого полнотекстого поиска"""

    name = filters.CharFilter(method="filter_name")

    def filter_name(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        query = Q(name__icontains=value)
        result = queryset.filter(query).distinct()
        if not result:
            vector = SearchVector(name, config="russian")
            query = SearchQuery(value, config="russian", search_type="phrase")
            for item in value.split(" "):
                query |= SearchQuery(item, config="russian", search_type="phrase")
            result = queryset.annotate(search=vector).filter(search=query).distinct()

        return result

    class Meta:
        model = Department
        fields = ["name"]
