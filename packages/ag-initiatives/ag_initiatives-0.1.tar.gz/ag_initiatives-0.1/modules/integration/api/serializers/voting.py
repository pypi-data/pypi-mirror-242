from rest_framework import serializers

from config.settings import DOMAIN_NAME, MEDIA_URL
from modules.api.serializers.voted_users_count_mixin import VotedUsersCountMixin
from modules.api.serializers.votes_count_mixin import VotesCountMixin
from modules.core.models import Locality, Department, Category, LocalityTypeEnum
from modules.voting.models import Vote, VoteAnswerOption
from modules.voting.models.vote_question import VoteQuestion


class CategoryVoteSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "color",
            "images",
        ]

    @staticmethod
    def get_images(obj):
        return [f"{DOMAIN_NAME}{MEDIA_URL}{image.file}" for image in obj.images.all()]


class LocalityVoteSerializer(serializers.ModelSerializer):
    locality_type = serializers.SerializerMethodField()

    class Meta:
        model = Locality
        fields = [
            "id",
            "name",
            "locality_type",
        ]

    @staticmethod
    def _get_first_key_by_value(value):
        keys = [k for k, v in LocalityTypeEnum.CHOICES if v == value]
        return keys[0] if keys else None

    def get_locality_type(self, obj):
        return self._get_first_key_by_value(obj.type.name) if obj.type else None


class DepartmentVoteSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "image",
            "email",
        ]

    @staticmethod
    def get_image(obj):
        return f"{DOMAIN_NAME}{MEDIA_URL}{obj.image}"


class VoteAnswerOptionIntegrationSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = VoteAnswerOption
        fields = [
            "id",
            "brief",
            "description",
            "image",
            "next_question_order",
            "order",
            "type",
        ]

    @staticmethod
    def get_image(obj):
        return f"{DOMAIN_NAME}{obj.image.link_from_model}" if obj.image and obj.image.link_from_model else None


class VoteQuestionSerializer(
    serializers.ModelSerializer, VotedUsersCountMixin, VotesCountMixin
):
    answers = VoteAnswerOptionIntegrationSerializer(many=True, read_only=True)
    photo = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = VoteQuestion
        fields = [
            "id",
            "brief",
            "description",
            "photo",
            "video",
            "file",
            "is_custom_answer_allowed",
            "custom_answer_length",
            "is_multi_answer_allowed",
            "max_answer_option_count",
            "order",
            "voted_users_count",
            "use_question_branches",
            "votes_count",
            "answers",
            "always_visible",
        ]

    @staticmethod
    def get_photo(obj):
        return f"{DOMAIN_NAME}{obj.photo.link_from_model}" if obj.photo and obj.photo.link_from_model else None

    @staticmethod
    def get_video(obj):
        return f"{DOMAIN_NAME}{obj.video.link_from_model}" if obj.video and obj.video.link_from_model else None

    @staticmethod
    def get_file(obj):
        return f"{DOMAIN_NAME}{obj.file.link_from_model}" if obj.file and obj.file.link_from_model else None


class VoteListSerializer(serializers.ModelSerializer):
    department = DepartmentVoteSerializer()
    category = CategoryVoteSerializer()
    state = serializers.CharField()
    image = serializers.SerializerMethodField()
    brief_image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    locality = LocalityVoteSerializer(many=True)
    questions = VoteQuestionSerializer(many=True)
    user_has_voted = serializers.BooleanField(required=False)

    class Meta:
        model = Vote
        fields = [
            "id",
            "url",
            "name",
            "topic",
            "start_date",
            "end_date",
            "state",
            "description_vote",
            "not_bonus_eligible",
            "author",
            "department",
            "category",
            "locality",
            "type_publication_with_group_restriction",
            "participants_groups",
            "participants_categories",
            "multi_locality_vote",
            "type_publication_with_age_restriction",
            "age_restriction_start",
            "age_restriction_finish",
            "multi_locality_vote",
            "is_opened",
            "is_published",
            "creation_date",
            "brief_image",
            "image",
            "video",
            "file",
            "custom_url",
            "to_moderation_date",
            "moderation_date",
            "operator_action_date",
            "reject_reason_text",
            "reject_reason_text_comment",
            "operator_reject_reason_text",
            "not_bonus_eligible",
            "bonus_amount",
            "questions",
            "user_has_voted",
        ]

    @staticmethod
    def get_url(obj):
        return f"{DOMAIN_NAME}/voting/details/{obj.id}"

    @staticmethod
    def get_image(obj):
        return f"{DOMAIN_NAME}{obj.image.link_from_model}" if obj.image and obj.image.link_from_model else None

    @staticmethod
    def get_brief_image(obj):
        return f"{DOMAIN_NAME}{obj.brief_image.link_from_model}" if obj.brief_image and obj.brief_image.link_from_model else None

    @staticmethod
    def get_video(obj):
        return f"{DOMAIN_NAME}{obj.video.link_from_model}" if obj.video and obj.video.link_from_model else None

    @staticmethod
    def get_file(obj):
        return f"{DOMAIN_NAME}{obj.file.link_from_model}" if obj.file and obj.file.link_from_model else None
