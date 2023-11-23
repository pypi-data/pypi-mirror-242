from rest_framework import serializers

from modules.api.serializers import LocalityShortSerializer
from modules.ecology.api.serializers import UserBalanceOperationSerializer
from modules.ecology.api.serializers.user_purchase import UserPurchaseSerializer
from modules.ecology.api.serializers.participation import (
    ParticipationUserListSerializer,
)
from modules.ecology.models import Notification
from modules.initiatives.models import Initiative
from modules.voting.models import Vote


class EcologyInitiativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initiative
        fields = [
            "id",
            "title",
            "number",
            "description",
        ]


class EcologyVoteSerializer(serializers.ModelSerializer):
    locality = LocalityShortSerializer(many=True)

    class Meta:
        model = Vote
        fields = [
            "id",
            "name",
            "locality",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    user_balance_operation = UserBalanceOperationSerializer()
    participation = ParticipationUserListSerializer()
    user_purchase = UserPurchaseSerializer()
    initiative = EcologyInitiativeSerializer()
    vote = EcologyVoteSerializer()

    class Meta:
        model = Notification
        fields = "__all__"
