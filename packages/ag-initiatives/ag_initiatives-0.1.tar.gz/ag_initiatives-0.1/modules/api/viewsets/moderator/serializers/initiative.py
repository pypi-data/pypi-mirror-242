from rest_framework import serializers

from modules.api.serializers import (
    InitiativeCategoryDetailedSerializer,
    LocalityShortSerializer,
)
from modules.api.serializers.locality import LocalityWithParentSerializer
from modules.initiatives.models import Initiative


class InitiativeForModeratorSerializer(serializers.ModelSerializer):
    category = InitiativeCategoryDetailedSerializer()
    locality = LocalityShortSerializer(many=True)
    creation_date_time = serializers.DateTimeField()
    state = serializers.CharField(source='get_state_display')
    title = serializers.CharField()
    messages_count = serializers.IntegerField()
    description = serializers.CharField()
    localities = LocalityWithParentSerializer(source='locality', many=True)

    class Meta:
        model = Initiative
        fields = (
            "id",
            "number",
            "type",
            "creation_date_time",
            "state",
            "localities",
            "locality",

            "title",
            "category",
            "messages_count",
            "description"
        )
