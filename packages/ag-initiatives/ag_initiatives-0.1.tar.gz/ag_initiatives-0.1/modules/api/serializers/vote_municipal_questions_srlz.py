from typing import Optional

from rest_framework import serializers

from modules.api.serializers import VoteMunicipalAnswerSerializer, FileField
from modules.voting.models import VoteMunicipalQuestion, UserMunicipalVote
from .voted_users_count_mixin import VotedUsersCountMixin
from .votes_count_mixin import VotesCountMixin
from ...core.models import User


class VoteMunicipalQuestionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    answers = VoteMunicipalAnswerSerializer(many=True, read_only=True, source="municipal_answers")
    photo = FileField()
    my_answers = serializers.SerializerMethodField()

    class Meta:
        model = VoteMunicipalQuestion
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

    def get_my_answers(self, instance: VoteMunicipalQuestion):
        user: Optional[User] = self.context.get("user", None)
        if not user:
            return None
        user_answers = UserMunicipalVote.objects.filter(user=user, question=instance)
        data = []
        for answer in user_answers:
            data.append({
                "answer_option": answer.answer_option.pk,
                "custom_answer": answer.custom_answer,
            })
        return data
