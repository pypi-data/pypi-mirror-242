import django_filters

from modules.voting.models import LocalVotingGroup


class LocalVotingGroupFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = LocalVotingGroup
        fields = [
            "access_token",
            "name",
        ]
