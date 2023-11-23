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
)
from modules.voting.models import VoteMunicipal, VoteMunicipalQuestion, VoteMunicipalAnswer, VoteState


class MunicipalVoteListSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    category = CategoryListSerializer()
    locality = serializers.SerializerMethodField()
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    brief_image = FileField()
    image = FileField()

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
            "state",
            "state_str",
            "voted_users_count",
            "use_question_branches",
        ]

    def get_state_str(self, instance: VoteMunicipal):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )

    def get_locality(self, vote: VoteMunicipal):
        return LocalityListSerializer(
            vote.locality.order_by("order", "name"), many=True
        ).data


class MunicipalVoteAnswerSerializer(
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
        ]


class MunicipalVoteQuestionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    answers = MunicipalVoteAnswerSerializer(many=True, read_only=True, source="municipal_answers")
    photo = FileField()

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
            "answers",
            "voted_users_count",
            "votes_count",
        ]


class MunicipalVoteDetailsSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    questions = MunicipalVoteQuestionSerializer(many=True, read_only=True, source="municipal_questions")
    category = CategoryListSerializer()
    locality = serializers.SerializerMethodField()
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    image = FileField()

    class Meta:
        model = VoteMunicipal
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
            "multi_municipality_vote",
            "description_vote",
            "vote_category",
            "type_publication_with_group_restriction",
            "age_restriction_start",
            "age_restriction_finish",
            "type_publication_with_age_restriction",
            "access_interim_results",
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

    def get_state_str(self, instance: VoteMunicipal):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )

    def get_locality(self, vote: VoteMunicipal):
        return LocalityListSerializer(
            vote.locality.order_by("order", "name"), many=True
        ).data


class MunicipalVoteCreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteMunicipalAnswer
        fields = [
            "brief",
            "description",
            "image",
            "order",
            "next_question_order",
            "type",
        ]


class MunicipalVoteCreateQuestionSerializer(serializers.ModelSerializer):
    answers = MunicipalVoteCreateAnswerSerializer(many=True, required=False, source="municipal_answers")

    class Meta:
        model = VoteMunicipalQuestion
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


class MunicipalVoteCreateSerializer(serializers.ModelSerializer):
    questions = MunicipalVoteCreateQuestionSerializer(many=True)

    class Meta:
        model = VoteMunicipal
        fields = [
            "name",
            "department",
            "municipal_formation",
            "locality",
            "category",
            "brief_image",
            "start_date",
            "end_date",
            "multi_municipality_vote",
            "description_vote",
            "vote_category",
            "type_publication_with_group_restriction",
            "age_restriction_start",
            "age_restriction_finish",
            "type_publication_with_age_restriction",
            "access_interim_results",
            "is_opened",
            "topic",
            "is_published",
            "image",
            "custom_url",
            "questions",
            "use_question_branches",
        ]


########################################################################################################################


class MunicipalVoteUpdateAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    image_details = FileShortSerializer(read_only=True, source="image")

    class Meta:
        model = VoteMunicipalAnswer
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


class MunicipalVoteUpdateQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    answers = MunicipalVoteUpdateAnswerSerializer(many=True, required=False, source="municipal_answers")
    photo_details = FileShortSerializer(read_only=True, source="photo")

    class Meta:
        model = VoteMunicipalQuestion
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


class MunicipalVoteUpdateSerializer(serializers.ModelSerializer):
    questions = MunicipalVoteUpdateQuestionSerializer(many=True, source="municipal_questions")
    department = DepartmentShortSerializer(read_only=True)
    image_details = FileShortSerializer(read_only=True, source="image")
    brief_image_details = FileShortSerializer(read_only=True, source="brief_image")

    class Meta:
        model = VoteMunicipal
        fields = [
            "id",
            "name",
            "category",
            "locality",
            "municipal_formation",
            "multi_municipality_vote",
            "department",
            "is_opened",
            "topic",
            "is_published",
            "start_date",
            "end_date",
            "image",
            "brief_image",
            "image_details",
            "brief_image_details",
            "custom_url",
            "questions",
            "use_question_branches",
        ]
