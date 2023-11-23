from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from modules.integration.models import UserSynchronization


class UserSynchronizationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user_id")

    class Meta:
        model = UserSynchronization
        fields = ("id", "synchorized_user_id", "external_system")
        validators = [
            UniqueTogetherValidator(
                queryset=UserSynchronization.objects.all(),
                fields=['id', 'synchorized_user_id', 'external_system']
            )
        ]
