from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from modules.api.serializers import LocalityShortSerializer
from modules.appeals.api.serializers import (
    CategoryDetailedSerializer,
    FileShortSerializer,
    ContractorSerializer,
    AppealResponseSerializer,
    GeoJSONField,
)
from modules.appeals.models import (
    Appeal,
    AppealOwnerCommunications,
    AppealOwnerCommunicationType,
)


class AppealOperatorListSerializer(serializers.ModelSerializer):
    locality = LocalityShortSerializer()
    category = CategoryDetailedSerializer()

    class Meta:
        model = Appeal
        fields = [
            "id",
            "creation_date_time",
            "create_by_operator",
            "state_name",
            "number",
            "locality",
            "category",
            "moderation_pass_date",
        ]


class AppealOperatorDetailsSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    author_patronymic_name = serializers.SerializerMethodField()
    category = CategoryDetailedSerializer()
    gis_point = GeoJSONField()
    files = FileShortSerializer(many=True)
    locality = LocalityShortSerializer()
    contractors = ContractorSerializer(many=True)
    response = AppealResponseSerializer()

    class Meta:
        model = Appeal
        fields = [
            "id",
            "creation_date_time",
            "create_by_operator",
            "state_name",
            "state",
            "number",
            "locality",
            "moderation_pass_date",
            "in_progress_begin_date",
            "responded_date",
            "contractors",
            "response",
            "author_first_name",
            "author_last_name",
            "author_patronymic_name",
            "email",
            "phone_number",
            "category",
            "description",
            "files",
            "address",
            "gis_point",
            "is_public",
        ]

    def get_author_first_name(self, instance: Appeal):
        return instance.user.first_name or ""

    def get_author_patronymic_name(self, instance: Appeal):
        return instance.user.patronymic_name or ""

    def get_author_last_name(self, instance: Appeal):
        return instance.user.last_name if instance.user.last_name else ""


class AppealInProgressOperatorSerializer(serializers.Serializer):
    contractors = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True
    )


class AppealOperatorCreateSerializer(serializers.ModelSerializer):
    applicant_first_name = serializers.CharField(required=True)
    applicant_patronymic_name = serializers.CharField(required=True, allow_blank=True)
    applicant_last_name = serializers.CharField(required=True)

    gis_point = GeoJSONField(required=False, allow_null=True)

    files = serializers.ListField(allow_null=True, allow_empty=True)

    class Meta:
        model = Appeal
        fields = [
            "applicant_first_name",
            "applicant_patronymic_name",
            "applicant_last_name",
            "phone_number",
            "locality",
            "category",
            "description",
            "files",
            "address",
            "gis_point",
            "is_public",
        ]


class AppealOwnerCommunicationsOperatorSerializer(serializers.ModelSerializer):
    files = FileShortSerializer(many=True)
    appeal_number = serializers.SerializerMethodField()
    comment = serializers.CharField(source="text")
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = AppealOwnerCommunications
        fields = [
            "appeal",
            "comment",
            "files",
            "timestamp",
            "type",
            "appeal_number",
            "user_name",
        ]

    def get_appeal_number(self, instance: AppealOwnerCommunications):
        return instance.appeal.number

    def get_user_name(self, instance: AppealOwnerCommunications):
        return (
            f"{instance.appeal.user.last_name} {instance.appeal.user.first_name} {instance.appeal.user.patronymic_name}"
            if instance.type == AppealOwnerCommunicationType.RESPONSE
            else "Модератор"
        )
