from rest_framework import serializers

from modules.api.serializers import (
    DepartmentShortSerializer,
    FileShortSerializer,
    VotedUsersCountMixin,
    VotesCountMixin,
)
from modules.core.models import Video
from modules.voting.api.serializers import (
    CategoryListSerializer,
    LocalityListSerializer, CategoryDetailsSerializer,
)
from modules.voting.models import Vote, VoteQuestion, VoteAnswerOption, VoteState


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class VoteModeratorListSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    category = CategoryDetailsSerializer()
    locality = serializers.SerializerMethodField()
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    image = FileShortSerializer()
    video = VideoSerializer()
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


class VoteModeratorAnswerOptionSerializer(
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


class VoteModeratorQuestionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    answers = VoteModeratorAnswerOptionSerializer(many=True, read_only=True)
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
            "answers",
            "voted_users_count",
            "votes_count",
            "video",
            "file",
            "custom_answer_length",
            "use_question_branches",
            "custom_answer_length",
        ]


class VoteModeratorDetailsSerializer(serializers.ModelSerializer, VotedUsersCountMixin):
    questions = VoteModeratorQuestionSerializer(many=True, read_only=True)
    category = CategoryDetailsSerializer()
    locality = serializers.SerializerMethodField()
    department = DepartmentShortSerializer()
    state_str = serializers.SerializerMethodField()
    image = FileShortSerializer()
    video = VideoSerializer()
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
            "questions",
            "state_str",
            "state",
            "reject_reason_text",
            "reject_reason_text_comment",
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
            "answer_description",
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

    def get_locality(self, vote):
        return LocalityListSerializer(
            vote.locality.order_by("order", "name"), many=True
        ).data
    

class VoteModeratorCreateAnswerOptionSerializer(serializers.ModelSerializer):
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


class VoteModeratorCreateQuestionSerializer(serializers.ModelSerializer):
    answers = VoteModeratorCreateAnswerOptionSerializer(many=True, required=False)

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


# class VoteModeratorCreateSerializer(serializers.ModelSerializer):
#     questions = VoteModeratorCreateQuestionSerializer(many=True)
#
#     class Meta:
#         model = Vote
#         fields = [
#             'name',
#             'category',
#             'locality',
#             'is_opened',
#             'topic',
#             'is_published',
#             'start_date',
#             'end_date',
#             # 'image',
#             'custom_url',
#             'questions',
#         ]


########################################################################################################################


class VoteModeratorUpdateAnswerOptionSerializer(serializers.ModelSerializer):
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


class VoteModeratorUpdateQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    answers = VoteModeratorUpdateAnswerOptionSerializer(many=True, required=False)
    photo_details = FileShortSerializer(read_only=True, source="photo")
    video_details = VideoSerializer(read_only=True, source="video")
    file_details = FileShortSerializer(read_only=True, source="file")

    class Meta:
        model = VoteQuestion
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
            "video",
            "video_details",
            "file",
            "file_details",
            "custom_answer_length",
            "use_question_branches",
            "custom_answer_length",
        ]


class VoteModeratorUpdateSerializer(serializers.ModelSerializer):
    questions = VoteModeratorUpdateQuestionSerializer(many=True, required=False)
    department = DepartmentShortSerializer(read_only=True)
    image_details = FileShortSerializer(read_only=True, source="image")
    brief_image_details = FileShortSerializer(read_only=True, source="brief_image")
    video_details = VideoSerializer(read_only=True, source="video")
    file_details = FileShortSerializer(read_only=True, source="file")

    class Meta:
        model = Vote
        fields = [
            "id",
            "name",
            "category",
            "department",
            "locality",
            "multi_locality_vote",
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

    def to_representation(self, instance):
        return VoteModeratorDetailsSerializer(instance, context=self.context).data
