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
    MunicipalityListSerializer,
)
from modules.voting.models import VoteRegional, VoteRegionalQuestion, VoteRegionalAnswer, VoteState


class RegionalVoteListSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    category = CategoryListSerializer()
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    brief_image = FileField()
    image = FileField()

    class Meta:
        model = VoteRegional
        fields = [
            "id",
            "name",
            "department",
            "category",
            "municipal_formation",
            "is_opened",
            "topic",
            "start_date",
            "end_date",
            "brief_image",
            "custom_url",
            "state",
            "state_str",
            "voted_users_count",
            "image",
            "use_question_branches",
        ]

    def get_state_str(self, instance: VoteRegional):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )


class RegionalVoteAnswerSerializer(
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
        ]


class RegionalVoteQuestionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    answers = RegionalVoteAnswerSerializer(many=True, read_only=True, source="regional_answers")
    photo = FileField()

    class Meta:
        model = VoteRegionalQuestion
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


class RegionalVoteDetailsSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    questions = RegionalVoteQuestionSerializer(many=True, read_only=True, source="municipal_questions")
    category = CategoryListSerializer()
    department = DepartmentShortSerializer()
    municipal_formation = MunicipalityListSerializer(many=True)
    state_str = serializers.SerializerMethodField()
    image = FileField()

    class Meta:
        model = VoteRegional
        fields = [
            "id",
            "name",
            "department",
            "municipal_formation",
            "category",
            "brief_image",
            "start_date",
            "end_date",
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

    def get_state_str(self, instance: VoteRegional):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )


class RegionalVoteCreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteRegionalAnswer
        fields = [
            "brief",
            "description",
            "image",
            "order",
            "next_question_order",
            "type",
        ]


class RegionalVoteCreateQuestionSerializer(serializers.ModelSerializer):
    answers = RegionalVoteCreateAnswerSerializer(many=True, required=False, source="regional_answers")

    class Meta:
        model = VoteRegionalQuestion
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


class RegionalVoteCreateSerializer(serializers.ModelSerializer):
    questions = RegionalVoteCreateQuestionSerializer(many=True)

    class Meta:
        model = VoteRegional
        fields = [
            "name",
            "municipal_formation",
            "category",
            "brief_image",
            "start_date",
            "end_date",
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
            "use_question_branches",
        ]


########################################################################################################################


class RegionalVoteUpdateAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    image_details = FileShortSerializer(read_only=True, source="image")

    class Meta:
        model = VoteRegionalAnswer
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


class RegionalVoteUpdateQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    answers = RegionalVoteUpdateAnswerSerializer(many=True, required=False, source="regional_answers")
    photo_details = FileShortSerializer(read_only=True, source="photo")

    class Meta:
        model = VoteRegionalQuestion
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


class RegionalVoteUpdateSerializer(serializers.ModelSerializer):
    questions = RegionalVoteUpdateQuestionSerializer(many=True, source="regional_questions")
    department = DepartmentShortSerializer(read_only=True)
    image_details = FileShortSerializer(read_only=True, source="image")
    brief_image_details = FileShortSerializer(read_only=True, source="brief_image")

    class Meta:
        model = VoteRegional
        fields = [
            "id",
            "name",
            "department",
            "municipal_formation",
            "category",
            "brief_image_details",
            "start_date",
            "end_date",
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
            "image_details",
            "questions",
            "use_question_branches",
        ]
