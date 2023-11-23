from rest_framework import serializers

from modules.api.serializers import LocalityShortSerializer
from modules.api.serializers.organization import DepartmentAsOrganizationSerializer
from modules.ecology.api.serializers import EventCategorySerializer
from modules.ecology.api.serializers.coordinates import CoordinatesSerializer
from modules.ecology.models import Event


class EventListSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer()
    locality = LocalityShortSerializer()
    display_localities = LocalityShortSerializer(many=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "category",
            "locality",
            "reward",
            "start_date",
            "expiry_date",
            "start_time",
            "expiry_time",
            "address",
            "display_localities"
        ]


class EventDetailsSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer()
    locality = LocalityShortSerializer()
    organization = DepartmentAsOrganizationSerializer()
    coordinates = CoordinatesSerializer(
        source="object_coordinates",
    )
    display_localities = LocalityShortSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "address",
            "category",
            "coordinates",
            "description",
            "display_localities",
            "expiry_date",
            "expiry_publication_date",
            "expiry_time",
            "is_published",
            "locality",
            "maximum_participants",
            "multiple_participation",
            "name",
            "organization",
            "reward",
            "start_date",
            "start_publication_date",
            "start_time",
        )
