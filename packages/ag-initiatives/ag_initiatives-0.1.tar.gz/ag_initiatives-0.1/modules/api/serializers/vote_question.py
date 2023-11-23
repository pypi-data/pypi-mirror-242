from typing import Optional

from rest_framework import serializers

from modules.api.serializers import VoteAnswerOptionSerializer, FileField, FileShortSerializer
from modules.voting.models import VoteQuestion, UserVote
from .voted_users_count_mixin import VotedUsersCountMixin
from .votes_count_mixin import VotesCountMixin
from ...core.models import User, Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class VoteQuestionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    answers = VoteAnswerOptionSerializer(many=True, read_only=True)
    my_answers = serializers.SerializerMethodField()
    photo = FileShortSerializer()
    video = VideoSerializer()
    file = FileShortSerializer()

    class Meta:
        model = VoteQuestion
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
            "use_question_branches",
            "video",
            "file",
            "custom_answer_length",
        ]

    def get_my_answers(self, instance: VoteQuestion):
        user: Optional[User] = self.context.get("user", None)
        if not user:
            return None
        user_answers = UserVote.objects.filter(user=user, question=instance)
        data = []
        for answer in user_answers:
            data.append({
                "answer_option": answer.answer_option.pk,
                "custom_answer": answer.custom_answer,
            })
        return data
