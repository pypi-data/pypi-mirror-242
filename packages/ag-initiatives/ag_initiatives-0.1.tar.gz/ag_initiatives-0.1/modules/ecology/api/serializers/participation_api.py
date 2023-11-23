from rest_framework import serializers

from modules.ecology.models import Event


class OperatorEventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "category",
            "image",
            "start_date",
            "expiry_date",
            "address",
        ]


class OperatorEventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
