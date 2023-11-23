from rest_framework import serializers

from modules.ecology.models import EventCategory


class EventCategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = [
            "id",
            "name",
            "color",
            "image",
            "icon",
        ]


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"
