from rest_framework import serializers

from modules.api.serializers import (
    InitiativeCategoryDetailedSerializer,
    LocalityShortSerializer,
    DepartmentShortSerializer,
)
from modules.initiatives.models import Initiative


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = self.get_fields_for_user(kwargs.pop("user"))
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_fields_for_user(self, user):
        base_fields = ("id", "number", "creation_date_time", "state", "locality")
        if user.is_operator:
            fields = base_fields + (
                "title",
                "category",
                "date_of_report_publication",
                "date_of_decision",
                "is_additional",
                "department",
                "description"
            )
        elif user.is_moderator:
            fields = base_fields + ("title", "category", "messages_count", "description")
        else:
            fields = base_fields + ("is_published", "title", "description")
        return fields


class InitiativeForUserSerializer(DynamicFieldsModelSerializer):
    category = InitiativeCategoryDetailedSerializer()
    locality = LocalityShortSerializer(many=True)
    creation_date_time = serializers.DateTimeField()
    state = serializers.CharField(source='get_state_display')
    department = DepartmentShortSerializer(source='settings.department')
    is_additional = serializers.SerializerMethodField()
    messages_count = serializers.IntegerField()
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
            "is_published",
            "is_additional",
            "department",
            "messages_count",
            "description",
        )

    def get_is_additional(self, obj: Initiative):
        return False
        # return obj.is_additional
