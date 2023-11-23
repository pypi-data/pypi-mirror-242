from typing import Union, Literal

import django_filters
from django.db.models import Q, QuerySet

from modules.core.models import Category
# from modules.voting.enums import VoteType
from modules.voting.models import VoteLocal, LocalVotingGroup


class VoteLocalFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())

    access_token = django_filters.CharFilter(method="filter_access_token")

    def filter_access_token(
        self, queryset: QuerySet, name: Literal["access_token"], value: str
    ) -> Union[QuerySet, VoteLocal]:
        query = Q(access_token=value)
        local_voting_group = LocalVotingGroup.objects.filter(query).first()
        result = queryset.none()
        if local_voting_group:
            query = Q(pk=local_voting_group.vote.pk)
            result = VoteLocal.objects.filter(query).distinct()

        return result

    # vote_type = django_filters.ChoiceFilter(
    #     field_name="vote_type", choices=list(VoteType.choices())
    # )

    class Meta:
        model = VoteLocal
        fields = [
            "locality",
            "category",
            "is_opened",
        ]


class VoteLocalStatsFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = VoteLocal
        fields = [
            "locality",
            "category",
        ]
