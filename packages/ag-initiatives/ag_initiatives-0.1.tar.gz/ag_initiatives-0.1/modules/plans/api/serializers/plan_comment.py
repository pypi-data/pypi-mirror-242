from rest_framework import serializers

from modules.api.serializers import LocalitySerializer
from modules.core.models import User
from modules.plans.api.serializers import CategoryDetailedSerializer, LocationSerializer
from modules.plans.models import PlanComment, Plan


def _get_username(user: User):
    last_name = f"{user.last_name[0]}." if len(user.last_name) > 0 else ""
    return f"{user.first_name} {user.patronymic_name} {last_name}"


class PlanCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = PlanComment
        fields = [
            "username",
            "text",
            "timestamp",
        ]

    def get_username(self, obj: PlanComment):
        return _get_username(obj.user)


# для избежания циклической зависимости. todo: использовать PlanListSerializer из plan.py
class PlanListSerializer(serializers.ModelSerializer):
    category = CategoryDetailedSerializer()
    publication_date = serializers.DateTimeField(format="%Y-%m-%d")
    location = LocationSerializer(
        required=False, allow_null=True,
    )

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "category",
            "publication_date",
            "location",
        ]


class PlanCommentModeratorListSerializer(serializers.ModelSerializer):
    # plan = PlanListSerializer()
    locality = LocalitySerializer(source="plan.locality")
    username = serializers.SerializerMethodField()

    class Meta:
        model = PlanComment
        fields = [
            "id",
            "timestamp",
            "plan",
            "locality",
            "username",
        ]

    def get_username(self, obj: PlanComment):
        return _get_username(obj.user)


class PlanCommentModeratorListSerializer2(serializers.ModelSerializer):
    plan = PlanListSerializer()
    locality = LocalitySerializer(source="plan.locality")
    username = serializers.SerializerMethodField()

    class Meta:
        model = PlanComment
        fields = [
            "id",
            "timestamp",
            "plan",
            "locality",
            "username",
            "moderated",
        ]

    def get_username(self, obj: PlanComment):
        return _get_username(obj.user)


class PlanCommentModeratorSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = PlanComment
        fields = [
            "id",
            "text",
            "timestamp",
            "username",
            "moderated",
        ]

    def get_username(self, obj: PlanComment):
        return _get_username(obj.user)
