from typing import Union, Literal

import django_filters
from django.db.models import Q, QuerySet

from modules.core.models import Category
from modules.voting.enums import VoteType
from modules.voting.models import Vote, LocalVotingGroup


class VoteFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())

    access_token = django_filters.CharFilter(method="filter_access_token")

    def filter_access_token(
        self, queryset: QuerySet, name: Literal["access_token"], value: str
    ) -> Union[QuerySet, Vote]:
        query = Q(access_token=value)
        local_voting_group = LocalVotingGroup.objects.filter(query).first()
        result = queryset.none()
        if local_voting_group:
            query = Q(pk=local_voting_group.vote.pk)
            result = Vote.objects.filter(query).distinct()

        return result

    class Meta:
        model = Vote
        fields = [
            "locality",
            "category",
            "is_opened",
        ]


class VoteStatsFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Vote
        fields = [
            "locality",
            "category",
        ]
