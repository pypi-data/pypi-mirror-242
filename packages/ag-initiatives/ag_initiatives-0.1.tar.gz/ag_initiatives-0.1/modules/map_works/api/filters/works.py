import datetime

import django_filters
from django.db.models import Q
from django.utils import timezone
from pytz import utc

from modules.map_works.models import WorkCategory, Works
from modules.map_works.models import WorksState


class WorksFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=WorkCategory.objects.all()
    )
    state = django_filters.TypedMultipleChoiceFilter(
        choices=list(WorksState.CHOICES), method="filter_by__state"
    )
    completed_date_range = django_filters.DateTimeFromToRangeFilter(
        method="filter_by__completed_date_range"
    )
    department = django_filters.NumberFilter(
        method="filter_by__department"
    )

    class Meta:
        model = Works
        fields = [
            "locality",
            "category",
            "state",
            "completed_date_range",
            "department"
        ]

    def filter_by__state(self, queryset, name, value):
        now_time = timezone.now()
        q = Q()

        for state in set(value):
            if state == WorksState.PLANNED:
                q = q | Q(begin_datetime__gt=now_time)
            if state == WorksState.IN_PROGRESS:
                q = q | Q(begin_datetime__lte=now_time, end_datetime__gte=now_time)
            if state == WorksState.COMPLETED:
                q = q | Q(end_datetime__lt=now_time)

        return queryset.filter(q)

    def filter_by__completed_date_range(self, queryset, name, value):
        now_time = timezone.now()
        q = Q(end_datetime__lt=now_time)  # WorksState.COMPLETED
        q = q & (
            Q(begin_datetime__lte=value.stop.date() + datetime.timedelta(days=1))
            & Q(end_datetime__gte=value.start.date())
        )
        return queryset.filter(q)

    def filter_by__department(self, queryset, name, value: int):
        return queryset.filter(owner__id=value)
