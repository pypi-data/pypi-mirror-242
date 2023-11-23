import django_filters
from django.db.models import Q
from django.utils import timezone
from pydantic import ValidationError

from modules.map_works.models import WorksState


class MapWorksFilter(django_filters.FilterSet):
    """FilterSet для Дорожных работ:
    state -> str - method filter_state - можно перечислять через запятую
    """

    state = django_filters.CharFilter(method='filter_state')

    def filter_state(self, queryset, name, value):
        now_time = timezone.now()

        if "," not in value and ", " not in value:
            query = None
            if value == WorksState.PLANNED:
                query = Q(begin_datetime__gt=now_time)
            if value == WorksState.IN_PROGRESS:
                query = Q(begin_datetime__lte=now_time, end_datetime__gte=now_time)
            if value == WorksState.COMPLETED:
                query = Q(end_datetime__lt=now_time)

            if query is not None:
                return queryset.filter(query)
            return queryset.none()

        try:
            state_list = value.split(",")
            query = Q()
            for state in state_list:
                if state == WorksState.PLANNED:
                    query = query | Q(begin_datetime__gt=now_time)
                if state == WorksState.IN_PROGRESS:
                    query = query | Q(begin_datetime__lte=now_time, end_datetime__gte=now_time)
                if state == WorksState.COMPLETED:
                    query = query | Q(end_datetime__lt=now_time)
            return queryset.filter(query)

        except (ValueError, TypeError):
            raise ValidationError("Неккоректный фильтр статуса")