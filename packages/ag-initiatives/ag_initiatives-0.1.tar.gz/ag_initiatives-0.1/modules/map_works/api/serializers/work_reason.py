from rest_framework import serializers

from modules.map_works.models import WorkReason


class WorkReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkReason
        fields = "__all__"
