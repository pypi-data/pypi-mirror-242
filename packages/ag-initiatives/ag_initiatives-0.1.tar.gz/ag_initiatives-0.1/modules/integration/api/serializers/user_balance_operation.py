from rest_framework import serializers

from modules.ecology.models import UserBalanceOperation


class UserBalanceOperationSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='timestamp')

    class Meta:
        model = UserBalanceOperation
        fields = ("user_id", "date", "amount", "type", "target")
