from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from modules.api.serializers import (
    InitiativeCategoryShortSerializer,
    InitiativeCategoryDetailedSerializer,
    InitiativeFileShortSerializer,
    LocalityShortSerializer,
    DepartmentShortSerializer,
)
from modules.api.serializers.initiative_operator_communication import (
    InitiativeOperatorCommunicationSerializer,
)
from modules.api.serializers.locality import LocalityWithParentSerializer
from modules.initiatives.models import (
    Initiative,
    InitiativeFile,
    InitiativeAcceptingSettings,
)
from modules.initiatives.models.initiative_operator_communication import (
    ModerateResponseState,
)


class InitiativeShortSerializer(serializers.ModelSerializer):
    category = InitiativeCategoryDetailedSerializer()
    locality = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Initiative
        fields = [
            "id",
            "category",
            "vote_finish_date",
            "creation_date_time",
            "date_of_report_publication",
            "date_of_decision",
            "title",
            "type_name",
            "state_name",
            "votes_count",
            "votes_threshold",
            "locality",
        ]


class InitiativeOwnerShortSerializer(serializers.ModelSerializer):
    category = InitiativeCategoryShortSerializer()
    locality = LocalityShortSerializer(many=True)

    class Meta:
        model = Initiative
        fields = [
            "id",
            "creation_date_time",
            "number",
            "type_name",
            "state_name",
            "category",
            "locality",
            "is_published",
        ]


class InitiativeSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    author_patronymic_name = serializers.SerializerMethodField()
    category = InitiativeCategoryDetailedSerializer()
    files = InitiativeFileShortSerializer(many=True)
    is_owner = serializers.SerializerMethodField()
    is_voted = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField()
    communications = InitiativeOperatorCommunicationSerializer(many=True)
    department = serializers.SerializerMethodField()
    localities = LocalityWithParentSerializer(source='locality', many=True)

    class Meta:
        model = Initiative
        fields = [
            "id",
            "number",
            "type",
            "type_name",
            "state",
            "state_name",
            "author_first_name",
            "author_last_name",
            "author_patronymic_name",
            "author_email",
            "category",
            "locality",
            "localities",
            "title",
            "description",
            "expectations",
            "files",
            "vote_finish_date",
            "creation_date_time",
            "date_of_report_publication",
            "date_of_decision",
            "votes_count",
            "votes_threshold",
            "is_owner",
            "is_voted",
            "department",
            "communications",
        ]

    def get_author_first_name(self, instance: Initiative):
        return instance.user.first_name or ""

    def get_author_patronymic_name(self, instance: Initiative):
        return instance.user.patronymic_name or ""

    def get_author_last_name(self, instance: Initiative):
        return instance.user.last_name if instance.user.last_name else ""

    def get_author_email(self, instance: Initiative):
        return instance.email

    def get_department(self, instance: Initiative):
        department = getattr(instance.settings, "department", None)
        if department:
            return DepartmentShortSerializer(instance=department).data
        return None

    def get_is_owner(self, instance: Initiative):
        request = self.context.get("request", None)

        if request is None:
            return False

        return instance.is_owner(request.user)

    def get_is_voted(self, instance: Initiative):
        request = self.context.get("request", None)

        if request is None:
            return False

        return instance.is_voted(request.user)


class InitiativePrivateSerializer(InitiativeSerializer):
    communications = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeSerializer.Meta.model
        fields = InitiativeSerializer.Meta.fields

    def get_communications(self, instance: Initiative):
        qs = instance.communications
        if self.context["request"].user.is_operator:
            qs = qs.filter(
                ~Q(
                    state__in=[
                        ModerateResponseState.MODERATION_REQUIRED,
                        ModerateResponseState.REJECTED,
                    ]
                )
            )
        return InitiativeOperatorCommunicationSerializer(qs, many=True).data


class InitiativeCreateSerializer(serializers.ModelSerializer):
    files = serializers.ListField(allow_null=True, allow_empty=True)
    is_regional = serializers.BooleanField(
        allow_null=True,
        default=False,
    )

    class Meta:
        model = Initiative
        fields = [
            "email",
            "settings",
            "title",
            "description",
            "expectations",
            "files",
            "is_regional",
        ]

    def validate_files(self, files_id):
        if files_id:
            if InitiativeFile.objects.filter(pk__in=files_id).count() == len(files_id):

                return files_id
            raise ValidationError(
                {"detail": "Файла с таким идентификатором не существует."}
            )


class InitiativeUpdateSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()

    class Meta:
        model = Initiative
        fields = ("title", "description", "expectations", "files", "category")
        extra_kwargs = {"category": {"write_only": True}}

    @staticmethod
    def get_files(obj):
        files_id = obj.files.values_list('id', flat=True)
        if files_id:
            if InitiativeFile.objects.filter(pk__in=files_id).count() == len(files_id):

                return files_id
            raise ValidationError(
                {"detail": "Файла с таким идентификатором не существует."}
            )

    def validate(self, attrs):
        locality = self.instance.locality.values_list('id', flat=True)
        category = attrs["category"]
        settings = InitiativeAcceptingSettings.objects.filter(
            category=category, locality__in=locality, active=True
        ).first()
        if not settings:
            raise ValidationError(
                "Параметров приёма инициатив для вашего запроса не существует."
            )
        attrs["settings"] = settings
        attrs["votes_threshold"] = settings.votes_threshold
        attrs["duration_month"] = settings.duration_month
        return attrs
