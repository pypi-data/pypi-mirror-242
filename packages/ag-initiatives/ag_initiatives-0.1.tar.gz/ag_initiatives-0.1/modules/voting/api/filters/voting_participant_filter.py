from typing import Union

import django_filters
from django.db.models import QuerySet, Q

from modules.voting.models import VotingParticipant


class VotingParticipantFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(method="filter_full_name")

    def filter_full_name(
        self, queryset: QuerySet, name: str, value: str
    ) -> Union[QuerySet, VotingParticipant]:
        query = Q()
        for participant in queryset:
            if value.lower() in participant.full_name.lower():
                query |= Q(pk=participant.pk)
        result = queryset.filter(query).distinct()
        return result

    class Meta:
        model = VotingParticipant
        fields = [
            "last_name",
            "first_name",
            "patronymic_name",
            "email",
            "phone",
        ]
