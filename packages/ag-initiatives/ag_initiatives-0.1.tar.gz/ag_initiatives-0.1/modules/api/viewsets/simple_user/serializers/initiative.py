from rest_framework import serializers

from modules.api.serializers import (
    LocalityShortSerializer,
)
from modules.initiatives.models import Initiative


class InitiativeForSimpleUserSerializer(serializers.ModelSerializer):
    locality = LocalityShortSerializer(many=True)
    creation_date_time = serializers.DateTimeField()
    state = serializers.CharField(source='get_state_display')
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

            "is_published",
            "title",
            "description",
        )
