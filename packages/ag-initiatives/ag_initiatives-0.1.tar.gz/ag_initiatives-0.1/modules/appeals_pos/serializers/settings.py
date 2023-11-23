from rest_framework import serializers

from modules.appeals_pos.models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        exclude = ["id"]
