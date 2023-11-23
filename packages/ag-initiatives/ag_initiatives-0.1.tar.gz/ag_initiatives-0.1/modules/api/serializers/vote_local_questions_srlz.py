from typing import Optional

from rest_framework import serializers

from modules.api.serializers import FileField
from modules.voting.models import VoteLocalQuestion, UserMunicipalVote
from .voted_users_count_mixin import VotedUsersCountMixin
from .votes_count_mixin import VotesCountMixin
from ...core.models import User
from .vote_local_answer_srlz import VoteLocalAnswerSerializer


class VoteLocalQuestionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    answers = VoteLocalAnswerSerializer(many=True, read_only=True, source="local_answers")
    photo = FileField()
    my_answers = serializers.SerializerMethodField()

    class Meta:
        model = VoteLocalQuestion
        fields = [
            "id",
            "vote",
            "brief",
            "description",
            "photo",
            "is_custom_answer_allowed",
            "is_multi_answer_allowed",
            "max_answer_option_count",
            "voted_users_count",
            "votes_count",
            "order",
            "answers",
            "always_visible",
            "my_answers",
        ]

    def get_my_answers(self, instance: VoteLocalQuestion):
        user: Optional[User] = self.context.get("user", None)
        if not user:
            return None
        user_answers = UserMunicipalVote.objects.filter(user=user, question_loc=instance)
        data = []
        for answer in user_answers:
            data.append({
                "answer_option": answer.answer_option.pk,
                "custom_answer": answer.custom_answer,
            })
        return data
