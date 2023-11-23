from rest_framework import serializers

from modules.voting.models import VoteRegionalAnswer
from . import FileField
from .voted_users_count_mixin import VotedUsersCountMixin
from .votes_count_mixin import VotesCountMixin


class VoteRegionalAnswerSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    image = FileField()

    class Meta:
        model = VoteRegionalAnswer
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
