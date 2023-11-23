from rest_framework import serializers

from modules.api.serializers import (
    DepartmentShortSerializer,
    FileField,
    FileShortSerializer,
    VotedUsersCountMixin,
    VotesCountMixin,
)
from modules.voting.api.serializers import (
    CategoryListSerializer,
    LocalityListSerializer,
    MunicipalityListSerializer
)
from modules.voting.models import VoteLocal, VoteLocalQuestion, VoteLocalAnswer, VoteState


class LocalVoteListSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    category = CategoryListSerializer()
    locality = serializers.SerializerMethodField()
    municipal_formation = serializers.SerializerMethodField()
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    brief_image = FileField()
    image = FileField()

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
        ]

    def get_state_str(self, instance: VoteLocal):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )

    def get_locality(self, vote: VoteLocal):
        return LocalityListSerializer(
            vote.locality.order_by("order", "name"), many=True
        ).data

    def get_municipal_formation(self, vote: VoteLocal):
        return MunicipalityListSerializer(
            vote.municipal_formation.order_by("order", "name"), many=True
        ).data


class LocalVoteAnswerSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    image = FileField()

    class Meta:
        model = VoteLocalAnswer
        fields = [
            "id",
            "vote_question",
            "brief",
            "description",
            "image",
            "voted_users_count",
            "votes_count",
            "next_question_order",
        ]


class LocalVoteQuestionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    answers = LocalVoteAnswerSerializer(many=True, read_only=True, source="Local_answers")
    photo = FileField()

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
            "answers",
            "voted_users_count",
            "votes_count",
        ]


class LocalVoteDetailsSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    questions = LocalVoteQuestionSerializer(many=True, read_only=True, source="Local_questions")
    category = CategoryListSerializer()
    locality = serializers.SerializerMethodField()
    municipal_formation = serializers.SerializerMethodField()
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    image = FileField()

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
        ]

    def get_state_str(self, instance: VoteLocal):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )

    def get_locality(self, vote: VoteLocal):
        return LocalityListSerializer(
            vote.locality.order_by("order", "name"), many=True
        ).data

    def get_municipal_formation(self, vote: VoteLocal):
        return MunicipalityListSerializer(
            vote.municipal_formation.order_by("order", "name"), many=True
        ).data


class LocalVoteCreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteLocalAnswer
        fields = [
            "brief",
            "description",
            "image",
            "order",
            "next_question_order",
            "type",
        ]


class LocalVoteCreateQuestionSerializer(serializers.ModelSerializer):
    answers = LocalVoteCreateAnswerSerializer(many=True, required=False, source="local_answers")

    class Meta:
        model = VoteLocalQuestion
        fields = [
            "brief",
            "description",
            "photo",
            "is_custom_answer_allowed",
            "is_multi_answer_allowed",
            "max_answer_option_count",
            "answers",
            "order",
            "always_visible",
        ]


class LocalVoteCreateSerializer(serializers.ModelSerializer):
    questions = LocalVoteCreateQuestionSerializer(many=True)

    class Meta:
        model = VoteLocal
        fields = [
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
            "image",
            "custom_url",
            "questions",
            "use_question_branches",
        ]

########################################################################################################################


class LocalVoteUpdateAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    image_details = FileShortSerializer(read_only=True, source="image")

    class Meta:
        model = VoteLocalAnswer
        fields = [
            "id",
            "brief",
            "description",
            "image",
            "image_details",
            "order",
            "next_question_order",
            "type",
        ]


class LocalVoteUpdateQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    answers = LocalVoteUpdateAnswerSerializer(many=True, required=False, source="local_answers")
    photo_details = FileShortSerializer(read_only=True, source="photo")

    class Meta:
        model = VoteLocalQuestion
        fields = [
            "id",
            "brief",
            "description",
            "photo",
            "photo_details",
            "is_custom_answer_allowed",
            "is_multi_answer_allowed",
            "max_answer_option_count",
            "answers",
            "order",
            "always_visible",
        ]


class LocalVoteUpdateSerializer(serializers.ModelSerializer):
    questions = LocalVoteUpdateQuestionSerializer(many=True, source="local_questions")
    department = DepartmentShortSerializer(read_only=True)
    image_details = FileShortSerializer(read_only=True, source="image")
    brief_image_details = FileShortSerializer(read_only=True, source="brief_image")

    class Meta:
        model = VoteLocal
        fields = [
            "id",
            "name",
            "department",
            "municipal_formation",
            "locality",
            "category",
            "brief_image_details",
            "start_date",
            "end_date",
            "participants_groups",
            "description_vote",
            "access_interim_results",
            "access_total_results",
            "is_opened",
            "topic",
            "is_published",
            "image_details",
            "custom_url",
            "questions",
            "use_question_branches",
        ]