from rest_framework import serializers

from modules.ecology.models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = "__all__"
