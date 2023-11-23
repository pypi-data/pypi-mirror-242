import requests
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from django_filters import rest_framework as filters
from rest_framework import mixins, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.core.authentication_classes import ExternalSystemTokenAuthentication
from modules.core.models import Locality
from modules.ecology.models import Event, EventCategory
from modules.integration.api.filters.event import EventFilter
from modules.integration.api.serializers.event import EventSerializer, EventCreateSerializer, \
    EventForIntegrationUserSerializer
from modules.integration.permissions import CanGetSuggestions, CanTransmitSuggestions


class EventAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter
    serializer_class = EventSerializer
    authentication_classes = [ExternalSystemTokenAuthentication]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Event.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return EventCreateSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            return [CanTransmitSuggestions()]
        return [CanGetSuggestions()]

    @staticmethod
    def create_or_update_locality(request):
        if "locality" in request.data and (locality := request.data.pop("locality")):
            try:
                request.data["locality"] = Locality.objects.get(pk=locality.get("id")).id
            except Locality.DoesNotExist:
                request.data["locality"] = Locality.objects.create(
                    parent=locality.get("parent"),
                    name=locality.get("name"),
                    type_id=int(locality.get("type")),
                    gis_center=Point(
                        locality["gis_center"]["coordinates"][0],
                        locality["gis_center"]["coordinates"][1],
                    ) if locality.get("gis_center") else None
                ).id

    def create(self, request, *args, **kwargs):
        coord = request.data["coordinates"]
        request.data["coordinates"] = f"{coord['latitude']}, {coord['longitude']}"
        
        category_data = request.data.pop("category")

        self.create_or_update_locality(request)

        category_name = category_data["name"]
        if False:
            category_instance = ec_qs[0]
        else:
            image, icon = None, None

            if category_data.get("image"):
                image = category_data.pop("image")

            if category_data.get("icon"):
                icon = category_data.pop("icon")

            category_instance = EventCategory(
                **category_data,
            )

            if image and image != "null":
                image_name = image.split("/")[-1]
                response = requests.get(image, verify=False)
                category_instance.image.save(image_name, ContentFile(response.content), save=True)

            if icon and icon != "null":
                icon_name = icon.split("/")[-1]
                response = requests.get(icon, verify=False)
                category_instance.icon.save(icon_name, ContentFile(response.content), save=True)

            category_instance.save()

        request.data["category"] = category_instance.pk
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        coord = request.data["coordinates"]
        request.data["coordinates"] = f"{coord['latitude']}, {coord['longitude']}"

        # self.create_or_update_organization(request)
        self.create_or_update_locality(request)

        category_data = request.data.pop("category")
        image = category_data.pop("image", None)
        icon = category_data.pop("icon", None)
        category_data.pop("id", None)

        category_name = category_data["name"]
        if not (category_qs := EventCategory.objects.filter(name=category_name)):
            EventCategory.objects.create(name=category_name)
            category_qs = EventCategory.objects.filter(name=category_name)

        category_qs.update(**category_data)

        category_instance = category_qs[0]

        if image and category_instance.image != image and image != "null":
            image_name = image.split("/")[-1]
            response = requests.get(image, verify=False)
            category_instance.image.save(image_name, ContentFile(response.content), save=True)

        if icon and category_instance.icon != image and icon != "null":
            icon_name = icon.split("/")[-1]
            response = requests.get(icon, verify=False)
            category_instance.icon.save(icon_name, ContentFile(response.content), save=True)

        category_instance.save()

        request.data["category"] = category_instance.pk

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class EventForIntegrationByUserApi(EventAPI):
    serializer_class = EventForIntegrationUserSerializer
