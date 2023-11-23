from rest_framework import serializers

from modules.core.models import LkoInitiativeDescription


class LkoInitiativeDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LkoInitiativeDescription
        fields = ["description_id", "text", "initiative_type"]
