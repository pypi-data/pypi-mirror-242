from rest_framework import serializers

from modules.api.serializers import (
    DepartmentShortSerializer,
    FileShortSerializer,
    VotedUsersCountMixin,
    VotesCountMixin,
)
from modules.core.models import CategoryCitizen, File, Video
from modules.voting.api.serializers import (
    CategoryListSerializer,
    LocalityListSerializer, CategoryDetailsSerializer,
)
from modules.voting.models import Vote, VoteQuestion, VoteAnswerOption, VoteState


class VideoVoteOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class VoteOperatorListSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    category = CategoryDetailsSerializer()
    locality = serializers.SerializerMethodField()
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    image = FileShortSerializer(allow_null=True, required=False)
    video = VideoVoteOperatorSerializer(allow_null=True, required=False)
    file = FileShortSerializer(allow_null=True, required=False)

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

    def get_state_str(self, instance: Vote):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )

    def get_locality(self, vote: Vote):
        return LocalityListSerializer(
            vote.locality.order_by("order", "name"), many=True
        ).data


class VoteOperatorAnswerOptionSerializer(
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
        ]


class VoteOperatorQuestionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    answers = VoteOperatorAnswerOptionSerializer(many=True, read_only=True)
    photo = FileShortSerializer()
    video = VideoVoteOperatorSerializer()
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
            "answers",
            "voted_users_count",
            "votes_count",
            "video",
            "file",
            "custom_answer_length",
            "use_question_branches",
            "custom_answer_length",
        ]


class VoteOperatorDetailsSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    questions = VoteOperatorQuestionSerializer(many=True, read_only=True)
    category = CategoryDetailsSerializer()
    locality = serializers.SerializerMethodField()
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    image = FileShortSerializer()
    video = VideoVoteOperatorSerializer()
    file = FileShortSerializer()
    answer_description = serializers.SerializerMethodField(method_name="check_answer")

    class Meta:
        model = Vote
        fields = [
            "id",
            "name",
            "answer_description",
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
            "questions",
            "state_str",
            "state",
            "reject_reason_text",
            "reject_reason_text_comment",
            "moderation_date",
            "operator_action_date",
            "operator_reject_reason_text",
            "voted_users_count",
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
        
    def check_answer(self, instance: Vote):
        answer_description = False
        for question in instance.questions.all():
            for answer in question.answers.all():
                if answer.description != '':
                    answer_description = True
        return answer_description

    def get_state_str(self, instance: Vote):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )

    def get_locality(self, vote: Vote):
        return LocalityListSerializer(
            vote.locality.order_by("order", "name"), many=True
        ).data


class VoteOperatorCreateAnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteAnswerOption
        fields = [
            "brief",
            "description",
            "image",
            "order",
            "next_question_order",
            "type",
        ]


class VoteOperatorCreateQuestionSerializer(serializers.ModelSerializer):
    answers = VoteOperatorCreateAnswerOptionSerializer(many=True, required=False)

    class Meta:
        model = VoteQuestion
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
            "video",
            "file",
            "custom_answer_length",
            "use_question_branches",
            "custom_answer_length",
        ]


class EndDateField(serializers.DateTimeField):
    def to_internal_value(self, value):
        internal_value = super().to_internal_value(value)

        if internal_value:
            internal_value = internal_value.replace(hour=23, minute=59, second=59)

        return internal_value


class VoteOperatorCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    questions = VoteOperatorCreateQuestionSerializer(many=True)
    participants_categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CategoryCitizen.objects.all(),
        required=False,
    )
    end_date = EndDateField()

    class Meta:
        model = Vote
        fields = [
            "name",
            "category",
            "locality",
            "multi_locality_vote",
            "is_opened",
            "topic",
            "is_published",
            "start_date",
            "end_date",
            "image",
            "brief_image",
            "custom_url",
            "questions",
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


########################################################################################################################


class VoteOperatorUpdateAnswerOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    image_details = FileShortSerializer(read_only=True, source="image")

    class Meta:
        model = VoteAnswerOption
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


class VoteOperatorUpdateQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    answers = VoteOperatorUpdateAnswerOptionSerializer(many=True, required=False)
    file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True, required=False)
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all(), allow_null=True, required=False)
    photo = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True, required=False)

    class Meta:
        model = VoteQuestion
        fields = [
            "id",
            "brief",
            "description",
            "photo",
            "is_custom_answer_allowed",
            "is_multi_answer_allowed",
            "max_answer_option_count",
            "answers",
            "order",
            "always_visible",
            "video",
            "file",
            "custom_answer_length",
            "use_question_branches",
            "custom_answer_length",
        ]


class VoteOperatorUpdateSerializer(serializers.ModelSerializer):
    questions = VoteOperatorUpdateQuestionSerializer(many=True, required=False)
    department = DepartmentShortSerializer(read_only=True)
    image_details = FileShortSerializer(read_only=True, source="image")
    brief_image_details = FileShortSerializer(read_only=True, source="brief_image")
    video_details = VideoVoteOperatorSerializer(read_only=True, source="video")
    file_details = FileShortSerializer(read_only=True, source="file")
    state_str = serializers.SerializerMethodField()
    file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True, required=False)
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all(), allow_null=True, required=False)
    image = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Vote
        fields = [
            "id",
            "name",
            "category",
            "locality",
            "multi_locality_vote",
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
            "state",
            "state_str",
            "questions",
            "type_publication_with_group_restriction",
            "type_publication_with_age_restriction",
            "age_restriction_start",
            "age_restriction_finish",
            "video",
            "video_details",
            "file",
            "file_details",
            "description_vote",
            "participants_categories",
            "not_bonus_eligible",
            "bonus_amount",
            "author",
        ]

    @staticmethod
    def get_state_str(instance: Vote):
        return (
            VoteState.RESOLVER[instance.state]
            if instance.state in VoteState.RESOLVER
            else ""
        )

    def to_representation(self, instance):
        return VoteOperatorDetailsSerializer(instance, context=self.context).data
