from rest_framework import serializers

from modules.api.serializers import DepartmentShortSerializer
from modules.appeals.api.serializers import FileShortSerializer
from modules.appeals.models import AppealResponse


class AppealResponseShortSerializer(serializers.ModelSerializer):
    files = FileShortSerializer(many=True)
    responded_date = serializers.DateTimeField(source="appeal.responded_date")

    class Meta:
        model = AppealResponse
        fields = [
            "text",
            "files",
            "responded_date",
        ]


class AppealResponseSerializer(serializers.ModelSerializer):
    files = FileShortSerializer(many=True)
    department = DepartmentShortSerializer()
    responded_date = serializers.DateTimeField(source="appeal.responded_date")

    class Meta:
        model = AppealResponse
        fields = [
            "text",
            "files",
            "department",
            "responded_date",
        ]


class AppealResponseCreateSerializer(serializers.ModelSerializer):
    files = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, allow_null=True
    )

    class Meta:
        model = AppealResponse
        fields = [
            "text",
            "files",
        ]
