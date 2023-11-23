from rest_framework import serializers

from modules.appeals.api.serializers import (
    AppealUserListSerializer,
    AppealResponseSerializer,
)
from modules.appeals.models import AppealStateChange, AppealState
from modules.core.models import Department, UserRole


class NestedDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "image",
        ]


class AppealStateChangeSerializer(serializers.ModelSerializer):
    appeal = AppealUserListSerializer()
    user_role_name = serializers.SerializerMethodField()
    department = NestedDepartmentSerializer()
    appeal_id = serializers.IntegerField(source="appeal.pk")
    data = serializers.SerializerMethodField()

    class Meta:
        model = AppealStateChange
        fields = [
            "id",
            "appeal_id",
            "appeal",
            "new_state",
            "comment",
            "second_comment",
            "timestamp",
            "user",
            "user_role_name",
            "department",
            "data",
        ]

    def get_data(self, instance: AppealStateChange):
        return (
            AppealResponseSerializer(instance.appeal.response).data
            if instance.new_state == AppealState.RESPONDED
            else None
        )

    def get_user_role_name(self, instance: AppealStateChange):
        if instance.new_state == AppealState.MODERATION:
            return "Система"

        if instance.appeal.create_by_operator:
            return "Оператор"

        if instance.new_state in [
            AppealState.MODERATION_ACCEPTED,
            AppealState.MODERATION_REJECTED,
        ]:
            return "Модератор"

        if instance.new_state in [AppealState.IN_PROGRESS, AppealState.RESPONDED]:
            return instance.department.name if instance.department else "Оператор"

        return ""


class AppealStateChangeShortSerializer(serializers.ModelSerializer):
    user_role_name = serializers.SerializerMethodField()
    department = NestedDepartmentSerializer()
    appeal_id = serializers.IntegerField(source="appeal.pk")
    data = serializers.SerializerMethodField()

    class Meta:
        model = AppealStateChange
        fields = [
            "id",
            "appeal_id",
            "new_state",
            "comment",
            "second_comment",
            "timestamp",
            "user",
            "user_role_name",
            "department",
            "data",
        ]

    def get_data(self, instance: AppealStateChange):
        return (
            AppealResponseSerializer(instance.appeal.response).data
            if instance.new_state == AppealState.RESPONDED
            else None
        )

    def get_user_role_name(self, instance: AppealStateChange):
        if instance.new_state == AppealState.MODERATION:
            return "Система"

        if instance.appeal.create_by_operator:
            return "Оператор"

        if instance.new_state in [
            AppealState.MODERATION_ACCEPTED,
            AppealState.MODERATION_REJECTED,
        ]:
            return "Модератор"

        if instance.new_state in [AppealState.IN_PROGRESS, AppealState.RESPONDED]:
            return instance.department.name if instance.department else "Оператор"

        return ""
