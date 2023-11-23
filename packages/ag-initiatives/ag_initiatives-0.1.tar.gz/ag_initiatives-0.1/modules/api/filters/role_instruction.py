import django_filters
from rest_framework.exceptions import ValidationError


class RoleInstructionsFilter(django_filters.FilterSet):
    role = django_filters.CharFilter(method="filter_role")

    def filter_role(self, queryset, name, value: str):
        value = value.upper()
        if "," not in value:
            return queryset.filter(role=value)
        try:
            roles_string_list = value.split(",")
            return queryset.filter(role__in=roles_string_list)
        except (ValueError, TypeError):
            raise ValidationError("Неккоректный фильтр ролей")

