from rest_framework import serializers

from modules.initiatives.models import InitiativeRejectReason


class InitiativeRejectReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeRejectReason
        fields = ("id", "text")
