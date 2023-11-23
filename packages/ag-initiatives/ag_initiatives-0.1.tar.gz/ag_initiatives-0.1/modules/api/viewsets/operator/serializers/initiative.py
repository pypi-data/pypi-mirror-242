from rest_framework import serializers

from modules.api.serializers import (
    InitiativeCategoryDetailedSerializer,
    LocalityShortSerializer,
    DepartmentShortSerializer,
)
from modules.initiatives.models import Initiative


class InitiativeForOperatorSerializer(serializers.ModelSerializer):
    category = InitiativeCategoryDetailedSerializer()
    locality = LocalityShortSerializer(many=True)
    creation_date_time = serializers.DateTimeField()
    state = serializers.CharField(source='get_state_display')
    department = DepartmentShortSerializer(source='settings.department')
    is_additional = serializers.SerializerMethodField()
    title = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Initiative
        fields = (
            "id",
            "number",
            "creation_date_time",
            "state",
            "locality",

            "title",
            "category",
            "date_of_report_publication",
            "date_of_decision",
            "is_additional",
            "department",
            "description"
        )

    def get_is_additional(self, obj: Initiative):
        return False
        # return obj.is_additional
