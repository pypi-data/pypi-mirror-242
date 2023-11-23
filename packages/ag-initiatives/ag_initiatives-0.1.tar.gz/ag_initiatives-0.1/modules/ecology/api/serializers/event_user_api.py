from rest_framework import serializers

from modules.ecology.models import Event


class UserEventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "category",
            "start_date",
            "expiry_date",
            "address",
        ]


class UserEventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
