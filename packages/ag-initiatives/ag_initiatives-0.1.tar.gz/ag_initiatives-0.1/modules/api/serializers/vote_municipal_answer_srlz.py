from rest_framework import serializers

from modules.voting.models import VoteMunicipalAnswer
from . import FileField
from .voted_users_count_mixin import VotedUsersCountMixin
from .votes_count_mixin import VotesCountMixin


class VoteMunicipalAnswerSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    image = FileField()

    class Meta:
        model = VoteMunicipalAnswer
        fields = [
            "id",
            "vote_question",
            "brief",
            "description",
            "image",
            "voted_users_count",
            "votes_count",
            "next_question_order",
            "type",
        ]
