from rest_framework import serializers

from modules.api.serializers import (
    VoteQuestionSerializer,
    LocalityShortSerializer,
    DepartmentShortSerializer, FileShortSerializer
)
from modules.voting.models import Vote, UserVote, VoteState
from .category import CategoryShortSerializer
from .voted_users_count_mixin import VotedUsersCountMixin
from ...core.models import Video
from ...voting.api.serializers import CategoryDetailsSerializer
from ...voting.enums import VoteType


class VideoVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    user_has_voted = serializers.SerializerMethodField()
    category = CategoryDetailsSerializer()
    locality = LocalityShortSerializer(many=True)
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    image = FileShortSerializer()
    video = VideoVoteSerializer()
    file = FileShortSerializer()

    class Meta:
        model = Vote
        fields = [
            "id",
            "name",
            "department",
            "category",
            "locality",
            "multi_locality_vote",
            "is_opened",
            "topic",
            "start_date",
            "end_date",
            "brief_image",
            "image",
            "custom_url",
            "state",
            "state_str",
            "voted_users_count",
            "user_has_voted",
            "type_publication_with_group_restriction",
            "type_publication_with_age_restriction",
            "age_restriction_start",
            "age_restriction_finish",
            "video",
            "file",
            "description_vote",
            "participants_categories",
            "not_bonus_eligible",
            "bonus_amount",
            "author",
        ]

    def get_user_has_voted(self, vote: Vote):
        request = self.context["request"]

        if not request.user.is_authenticated:
            return False

        user_votes = UserVote.objects.filter(user=request.user, vote=vote)

        if not vote.multi_locality_vote:
            return user_votes.exists()

        locality_id = request.GET.get("locality", None)
        if locality_id is not None:
            return user_votes.filter(locality_id=locality_id).exists()
        else:
            return vote.locality.all().count() - user_votes.count() == 0

    def get_state_str(self, instance: Vote):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )


class VoteDetailsSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    user_has_voted = serializers.SerializerMethodField()
    # questions = VoteQuestionSerializer(many=True, read_only=True)
    questions = serializers.SerializerMethodField()
    category = CategoryDetailsSerializer()
    locality = LocalityShortSerializer(many=True)
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    image = FileShortSerializer()
    video = VideoVoteSerializer()
    file = FileShortSerializer()
    answer_description = serializers.SerializerMethodField(method_name="check_answer")

    class Meta:
        model = Vote
        fields = [
            "id",
            "name",
            "department",
            "category",
            "locality",
            "multi_locality_vote",
            "is_opened",
            "topic",
            "is_published",
            "start_date",
            "end_date",
            "image",
            "custom_url",
            "voted_users_count",
            "user_has_voted",
            "questions",
            "state",
            "state_str",
            "type_publication_with_group_restriction",
            "type_publication_with_age_restriction",
            "age_restriction_start",
            "age_restriction_finish",
            "video",
            "file",
            "description_vote",
            "participants_categories",
            "not_bonus_eligible",
            "bonus_amount",
            "author",
            "answer_description",
        ]

    def check_answer(self, instance: Vote):
        answer_description = False
        for question in instance.questions.all():
            for answer in question.answers.all():
                if answer.description != '':
                    answer_description = True
        return answer_description

    def get_questions(self, instance: Vote):
        return VoteQuestionSerializer(
            instance=instance.questions,
            many=True,
            read_only=True,
            context=self.context
        ).data


    def get_user_has_voted(self, obj: Vote):
        if self.context["request"].user.is_authenticated:
            request = self.context["request"]
            user_votes = UserVote.objects.filter(user=request.user, vote=obj)

            if obj.multi_locality_vote:
                locality_id = request.GET.get("locality", None)
                if locality_id is not None:
                    user_votes = user_votes.filter(locality_id=locality_id)

            return user_votes.exists()
        return False

    def get_state_str(self, instance: Vote):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )
