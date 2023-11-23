from rest_framework import serializers

from modules.api.serializers import (
    VoteMunicipalQuestionSerializer,
    LocalityShortSerializer,
    DepartmentShortSerializer,
    FileField,
)
from modules.voting.models import VoteMunicipal, UserMunicipalVote, VoteState
from .category import CategoryShortSerializer
from .voted_users_count_mixin import VotedUsersCountMixin
from ...voting.enums import VoteType


class VoteMunicipalSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    user_has_voted = serializers.SerializerMethodField()
    category = CategoryShortSerializer()
    locality = LocalityShortSerializer(many=True)
    department = DepartmentShortSerializer()
    brief_image = FileField()
    image = FileField()
    state_str = serializers.SerializerMethodField()

    class Meta:
        model = VoteMunicipal
        fields = [
            "id",
            "name",
            "department",
            "category",
            "locality",
            "municipal_formation",
            "multi_municipality_vote",
            "is_opened",
            "topic",
            "start_date",
            "end_date",
            "brief_image",
            "image",
            "custom_url",
            "voted_users_count",
            "user_has_voted",
            "state_str",
            "use_question_branches",
        ]

    def get_user_has_voted(self, vote: VoteMunicipal):
        request = self.context["request"]

        if not request.user.is_authenticated:
            return False

        user_votes = UserMunicipalVote.objects.filter(user=request.user, vote=vote)

        if not vote.multi_locality_vote:
            return user_votes.exists()

        locality_id = request.GET.get("locality", None)
        if locality_id is not None:
            return user_votes.filter(locality_id=locality_id).exists()
        else:
            return vote.locality.all().count() - user_votes.count() == 0

    def get_state_str(self, instance: VoteMunicipal):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )


class VoteMunicipalDetailsSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    user_has_voted = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    category = CategoryShortSerializer()
    locality = LocalityShortSerializer(many=True)
    department = DepartmentShortSerializer()
    image = FileField()
    state_str = serializers.SerializerMethodField()

    class Meta:
        model = VoteMunicipal
        fields = [
            "id",
            "name",
            "department",
            "category",
            "locality",
            "municipal_formation",
            "multi_municipality_vote",
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
            "state_str",
            "use_question_branches",
        ]

    def get_questions(self, instance: VoteMunicipal):
        return VoteMunicipalQuestionSerializer(
            instance=instance.questions,
            many=True,
            read_only=True,
            context=self.context
        ).data

    def get_user_has_voted(self, obj: VoteMunicipal):
        if self.context["request"].user.is_authenticated:
            request = self.context["request"]
            user_votes = UserMunicipalVote.objects.filter(user=request.user, vote=obj)

            if obj.multi_locality_vote:
                locality_id = request.GET.get("locality", None)
                if locality_id is not None:
                    user_votes = user_votes.filter(locality_id=locality_id)

            return user_votes.exists()
        return False

    def get_state_str(self, instance: VoteMunicipal):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )
