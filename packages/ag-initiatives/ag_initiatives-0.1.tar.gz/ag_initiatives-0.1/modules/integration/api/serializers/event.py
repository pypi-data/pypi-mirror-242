from rest_framework import serializers

from config.settings import DOMAIN_NAME, MEDIA_URL
from modules.core.models.locality import Locality
from modules.ecology.models import Event, EventCategory, ParticipationUserEvent
from modules.ecology.models.participation_user_event import ParticipationStatus
from modules.integration.api.serializers.locality import (LocalityIntegrationSerializer,
                                                          LocalityIntegrationShortSerializer)
from modules.integration.api.serializers.organization import DepartmentAsOrganizationIntegrationSerializer


class EventCategoryIntegrationSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = EventCategory
        fields = [
            "id",
            "name",
            "color",
            "image",
            "icon",
        ]

    @staticmethod
    def get_image(obj):
        return f"{DOMAIN_NAME}{MEDIA_URL}{obj.image}" if obj.image else None

    @staticmethod
    def get_icon(obj):
        return f"{DOMAIN_NAME}{MEDIA_URL}{obj.icon}" if obj.icon else None


class EventSerializer(serializers.ModelSerializer):
    category = EventCategoryIntegrationSerializer()
    organization = DepartmentAsOrganizationIntegrationSerializer()
    locality = LocalityIntegrationSerializer()
    coordinates = serializers.SerializerMethodField()
    display_localities = LocalityIntegrationShortSerializer(many=True)
    user_has_offer = serializers.BooleanField(required=False)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "url",
            "name",
            "description",
            "category",
            "organization",
            "locality",
            "reward",
            "multiple_participation",
            "maximum_participants",
            "start_date",
            "expiry_date",
            "start_time",
            "expiry_time",
            "start_publication_date",
            "expiry_publication_date",
            "address",
            "is_published",
            "coordinates",
            "display_localities",
            "user_has_offer",
        ]

    @staticmethod
    def get_url(obj):
        return f"{DOMAIN_NAME}/bonus/details/event/{obj.id}"

    @staticmethod
    def get_coordinates(obj):
        cord = obj.coordinates.split(", ") if obj.coordinates else [None, None]
        return {
            "latitude": cord[0],
            "longitude": cord[1],
        }


class EventForIntegrationUserSerializer(EventSerializer):
    status = serializers.SerializerMethodField()
    maximum_offer_usage = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "url",
            "name",
            "description",
            "category",
            "organization",
            "locality",
            "reward",
            "multiple_participation",
            "maximum_participants",
            "maximum_offer_usage",
            "start_date",
            "expiry_date",
            "start_time",
            "expiry_time",
            "start_publication_date",
            "expiry_publication_date",
            "address",
            "is_published",
            "coordinates",
            "display_localities",
            "user_has_offer",
            "status",
        ]

    def get_status(self, obj: Event):
        request = self.context.get('request')
        user_events = ParticipationUserEvent.objects.filter(event=obj, participant=request.user)
        if not user_events:
            return []
        return [
            {
                'id': event.id,
                'status': event.status
            }
            for event in user_events]

    @staticmethod
    def get_maximum_offer_usage(obj: Event) -> bool:
        if not obj.maximum_participants:
            return False
        return obj.maximum_participants <= ParticipationUserEvent.objects.filter(
            event=obj, status=ParticipationStatus.CONFIRMED).count()


class EventCreateSerializer(serializers.ModelSerializer):
    display_localities = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Locality.objects.all(), required=False
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "category",
            "organization",
            "locality",
            "reward",
            "multiple_participation",
            "maximum_participants",
            "start_date",
            "expiry_date",
            "start_time",
            "expiry_time",
            "start_publication_date",
            "expiry_publication_date",
            "address",
            "is_published",
            "display_localities",
            "coordinates",
        ]

    @staticmethod
    def get_coordinates(obj):
        cord = obj.coordinates.split(", ") if obj.coordinates else [None, None]
        return {
            "latitude": cord[0],
            "longitude": cord[1],
        }
