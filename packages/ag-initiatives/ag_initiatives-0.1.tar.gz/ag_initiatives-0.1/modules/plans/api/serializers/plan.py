from rest_framework import serializers

from modules.api.serializers import LocalitySerializer
from modules.api.serializers.locality import LocalityWithParentSerializer
from modules.plans.api.serializers import (
    CategorySerializer,
    FileSerializer,
    PlanCommentSerializer,
    CategoryDetailedSerializer,
    PlanCommentModeratorSerializer,
)
from modules.plans.api.serializers.location import LocationSerializer
from modules.plans.models import Plan


class PlanListSerializer(serializers.ModelSerializer):
    category = CategoryDetailedSerializer()
    publication_date = serializers.DateTimeField(format="%Y-%m-%d")
    location = LocationSerializer(
        required=False, allow_null=True,
    )
    locality = LocalityWithParentSerializer()

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "category",
            "publication_date",
            "location",
            "locality",
        ]
        ref_name = 'plan_list_serializer'


class PlanDetailsSerializer(serializers.ModelSerializer):
    locality = LocalitySerializer()
    category = CategorySerializer()
    publication_date = serializers.DateTimeField(format="%Y-%m-%d")
    location = LocationSerializer(
        required=False, allow_null=True,
    )
    files = FileSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "locality",
            "category",
            "publication_date",
            "description",
            "location",
            "files",
            "comments",
        ]

    def get_comments(self, plan: Plan):
        qs = plan.comments.filter(moderated=True).order_by("-timestamp")
        return PlanCommentSerializer(qs, many=True).data


class PlanDetails2Serializer(serializers.ModelSerializer):
    publication_date = serializers.DateTimeField(format="%Y-%m-%d")
    location = LocationSerializer(
        required=False, allow_null=True,
    )
    files = FileSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "locality",
            "category",
            "publication_date",
            "description",
            "location",
            "files",
            "comments",
        ]

    def get_comments(self, plan: Plan):
        qs = plan.comments.filter(moderated=True).order_by("-timestamp")
        return PlanCommentSerializer(qs, many=True).data


class PlanCreateSerializer(serializers.ModelSerializer):
    publication_date = serializers.DateTimeField(
        format="%Y-%m-%d", input_formats=["%Y-%m-%d"]
    )
    location = LocationSerializer(
        required=False, allow_null=True,
    )

    class Meta:
        model = Plan
        fields = [
            "name",
            "locality",
            "category",
            "publication_date",
            "description",
            "location",
            "files",
        ]


class PlanModeratorDetailsSerializer(serializers.ModelSerializer):
    locality = LocalitySerializer()
    category = CategorySerializer()
    publication_date = serializers.DateTimeField(format="%Y-%m-%d")
    location = LocationSerializer(
        required=False, allow_null=True,
    )
    files = FileSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "locality",
            "category",
            "publication_date",
            "description",
            "location",
            "files",
            "comments",
        ]

    def get_comments(self, plan: Plan):
        qs = plan.comments.order_by("-timestamp")
        return PlanCommentModeratorSerializer(qs, many=True).data
