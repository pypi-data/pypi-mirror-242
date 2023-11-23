from rest_framework import serializers

from modules.appeals.models import RejectReason


class RejectReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RejectReason
        fields = "__all__"
