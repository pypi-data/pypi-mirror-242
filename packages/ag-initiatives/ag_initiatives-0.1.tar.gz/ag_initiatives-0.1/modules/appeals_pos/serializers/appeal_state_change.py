from rest_framework import serializers

from modules.appeals_pos.models import AppealStateChange
from modules.appeals_pos.models.appeal import AppealState
from modules.appeals_pos.serializers.appeal_answer import AppealAnswerSerializer


class AppealStateChangeSerializer(serializers.ModelSerializer):
    answer = AppealAnswerSerializer()
    status_name = serializers.SerializerMethodField()

    class Meta:
        model = AppealStateChange
        fields = "__all__"

    def get_status_name(self, instance: AppealStateChange):
        return AppealState.RESOLVER.get(instance.status)
