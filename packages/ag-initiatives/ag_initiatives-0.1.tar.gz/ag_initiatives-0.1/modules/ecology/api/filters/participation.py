from typing import Union

import django_filters
from django.db.models import QuerySet, Q
from rest_framework.exceptions import ValidationError

from modules.ecology.models import ParticipationUserEvent
from modules.ecology.models.participation_user_event import ParticipationStatus


class ParticipationFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method="filter_status")

    def filter_status(
        self, queryset: Union[QuerySet, ParticipationUserEvent], name: str, value: str
    ) -> Union[QuerySet, ParticipationUserEvent]:
        if "," not in value:
            return queryset.filter(status=value.upper())
        query = Q()
        status_string_list = value.split(",")
        for status in status_string_list:
            if status.upper() in ParticipationStatus.RESOLVER.keys():
                query |= Q(status=status)
            else:
                raise ValidationError("Некорректный фильтр статуса")
        return queryset.filter(query)
