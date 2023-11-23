from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from modules.api.serializers import LocalityShortSerializer
from modules.appeals.api.serializers import (
    CategoryShortSerializer,
    FileShortSerializer,
    CategoryDetailedSerializer,
    AppealResponseSerializer,
    GeoJSONField,
)
from modules.appeals.models import Appeal


class AppealDetailsSerializer(serializers.ModelSerializer):
    category = CategoryDetailedSerializer()
    locality = LocalityShortSerializer()
    gis_point = GeoJSONField()
    files = FileShortSerializer(many=True)
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    author_patronymic_name = serializers.SerializerMethodField()
    response = AppealResponseSerializer()

    class Meta:
        model = Appeal
        fields = [
            "id",
            "category",
            "creation_date_time",
            "locality",
            "address",
            "gis_point",
            "state_name",
            "state",
            "author_first_name",
            "author_last_name",
            "author_patronymic_name",
            "description",
            "files",
            "response",
            "responded_date",
        ]

    def get_author_first_name(self, instance: Appeal):
        return instance.user.first_name or ""

    def get_author_patronymic_name(self, instance: Appeal):
        return instance.user.patronymic_name or ""

    def get_author_last_name(self, instance: Appeal):
        return instance.user.last_name if instance.user.last_name else ""


class AppealListSerializer(serializers.ModelSerializer):
    category = CategoryDetailedSerializer()
    gis_point = GeoJSONField()

    class Meta:
        model = Appeal
        fields = [
            "id",
            "category",
            "creation_date_time",
            "state_name",
            "address",
            "gis_point",
        ]
