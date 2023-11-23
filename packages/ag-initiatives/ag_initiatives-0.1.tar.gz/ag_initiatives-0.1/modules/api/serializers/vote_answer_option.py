from rest_framework import serializers

from modules.voting.models import VoteAnswerOption
from . import FileField, FileShortSerializer
from .voted_users_count_mixin import VotedUsersCountMixin
from .votes_count_mixin import VotesCountMixin


class VoteAnswerOptionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    image = FileShortSerializer()

    class Meta:
        model = VoteAnswerOption
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
