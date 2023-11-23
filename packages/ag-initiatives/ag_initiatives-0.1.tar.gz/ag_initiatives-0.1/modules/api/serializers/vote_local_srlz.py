from rest_framework import serializers

from modules.api.serializers import (
    LocalityShortSerializer,
    DepartmentShortSerializer,
    FileField,
)
from modules.voting.models import VoteLocal, UserMunicipalVote, VoteState
from .category import CategoryShortSerializer
from .voted_users_count_mixin import VotedUsersCountMixin
from .vote_local_questions_srlz import VoteLocalQuestionSerializer


class VoteLocalSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    user_has_voted = serializers.SerializerMethodField()
    category = CategoryShortSerializer()
    locality = LocalityShortSerializer(many=True)
    department = DepartmentShortSerializer()
    brief_image = FileField()
    image = FileField()
    state_str = serializers.SerializerMethodField()


    class Meta:
        model = VoteLocal
        fields = [
            "id",
            "name",
            "department",
            "category",
            "locality",
            "municipal_formation",
            "is_opened",
            "topic",
            "start_date",
            "end_date",
            "participants_groups",
            "brief_image",
            "image",
            "custom_url",
            "state",
            "state_str",
            "voted_users_count",
            "use_question_branches",
            "user_has_voted",
        ]
    
    def get_user_has_voted(self, vote: VoteLocal):
        request = self.context["request"]

        if not request.user.is_authenticated:
            return False

        user_votes = UserMunicipalVote.objects.filter(user=request.user, vote_loc=vote)

        locality_id = request.GET.get("locality", None)
        if locality_id is not None:
            return user_votes.filter(locality_id=locality_id).exists()
        else:
            return vote.locality.all().count() - user_votes.count() == 0

    def get_state_str(self, instance: VoteLocal):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )


class VoteLocalDetailsSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    user_has_voted = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    category = CategoryShortSerializer()
    locality = LocalityShortSerializer(many=True)
    department = DepartmentShortSerializer()
    image = FileField()
    state_str = serializers.SerializerMethodField()

    class Meta:
        model = VoteLocal
        fields = [
            "id",
            "name",
            "department",
            "municipal_formation",
            "locality",
            "category",
            "brief_image",
            "start_date",
            "end_date",
            "participants_groups",
            "description_vote",
            "access_interim_results",
            "access_total_results",
            "is_opened",
            "topic",
            "is_published",
            "custom_url",
            "image",
            "questions",
            "state_str",
            "state",
            "reject_reason_text",
            "reject_reason_text_comment",
            "moderation_date",
            "operator_action_date",
            "operator_reject_reason_text",
            "voted_users_count",
            "use_question_branches",
            "user_has_voted",
        ]

    def get_questions(self, instance: VoteLocal):
        return VoteLocalQuestionSerializer(
            instance=instance.questions,
            many=True,
            read_only=True,
            context=self.context
        ).data


    def get_user_has_voted(self, obj: VoteLocal):
        if self.context["request"].user.is_authenticated:
            request = self.context["request"]
            user_votes = UserMunicipalVote.objects.filter(user=request.user, vote_loc=obj)
            return user_votes.exists()
        return False

    def get_state_str(self, instance: VoteLocal):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )
