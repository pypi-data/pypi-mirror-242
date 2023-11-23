from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from config.settings import settings
from modules.api.serializers import (
    InitiativeFileShortSerializer,
    DepartmentShortSerializer,
)
from modules.core.models import User
from modules.initiatives.models import InitiativeOperatorCommunication
from modules.initiatives.models.initiative_operator_communication import (
    ModerateResponseState,
)


class InitiativeOperatorCommunicationSerializer(serializers.ModelSerializer):
    initiator = serializers.SerializerMethodField()
    files = InitiativeFileShortSerializer(many=True)
    department = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeOperatorCommunication
        fields = "__all__"

    def get_initiator(self, obj):
        user: User = getattr(obj, "user", None)
        if user:
            sub_permissions = getattr(user, "sub_permissions", None)
            if user.is_operator and getattr(sub_permissions, "operator_permissions", None):
                department = getattr(user.sub_permissions.operator_permissions, "department", None)
                return department.name if department is not None else str(user)
            elif user.is_moderator:
                return "Модератор"
            elif (
                    user.is_simple_user
                    and user.esia_id in settings.INITIATIVES_HIDE_USERNAME
            ):
                return "Оператор"
            elif user.is_simple_user:
                return str(user)

    def get_department(self, obj):
        if obj.user:
            department = None
            sub_permissions = getattr(obj.user, "sub_permissions", None)
            if obj.user.is_operator and getattr(sub_permissions, "operator_permissions", None):
                department = getattr(obj.user.sub_permissions.operator_permissions, "department", None)
            if obj.user.is_moderator:
                department = getattr(obj.user, "department", None)
            if obj.user.is_admin_lko and getattr(sub_permissions, "admin_lko_permissions", None):
                department = getattr(obj.user.sub_permissions.admin_lko_permissions, "department", None)
            if department is not None:
                return DepartmentShortSerializer(department).data
            else:
                return department


class InitiativeOperatorCommunicationListSerializer(
    InitiativeOperatorCommunicationSerializer
):
    initiative = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeOperatorCommunicationSerializer.Meta.model
        fields = InitiativeOperatorCommunicationSerializer.Meta.fields

    def get_initiative(self, obj):
        return {
            "id": obj.initiative.id,
            "number": obj.initiative.number,
        }


class InitiativeCommunicationModerationSerializer(serializers.ModelSerializer):
    state = serializers.CharField()

    class Meta:
        model = InitiativeOperatorCommunication
        fields = ("state",)

    def validate_state(self, value):
        if value not in (
                ModerateResponseState.APPROVED,
                ModerateResponseState.REJECTED,
        ):
            raise ValidationError()
        return value

    def update(self, instance, validated_data):
        instance.state = validated_data["state"]
        instance.moderator_viewed = True
        instance.save()
        return instance
