from rest_framework import serializers

from modules.initiatives.models import InitiativeSettings


class InitiativeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeSettings
        fields = [
            "user_locality_check",
        ]
