import requests
from django.core.files.base import ContentFile
from rest_framework import mixins, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.core.authentication_classes import ExternalSystemTokenAuthentication
from modules.ecology.models import GoodsNServicesItem, GoodsNServicesItemCategory
from modules.integration.api.filters.reward import RewardFilter
from modules.integration.api.serializers.goodsnservicesitem import GoodsNServicesItemSerializer, \
    GoodsNServicesItemCreateSerializer, GoodsNServicesItemSerializerForIntegrationUser
from modules.integration.permissions import CanGetEncouragements, CanTransmitEncouragements


class GoodsNServicesItemAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = GoodsNServicesItemSerializer
    authentication_classes = [ExternalSystemTokenAuthentication]
    pagination_class = LimitOffsetPagination
    filterset_class = RewardFilter

    def get_queryset(self):
        return GoodsNServicesItem.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return GoodsNServicesItemCreateSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            return [CanTransmitEncouragements()]
        return [CanGetEncouragements()]

    def create(self, request, *args, **kwargs):

        coord = request.data["coordinates"]
        request.data["coordinates"] = f"{coord['latitude']}, {coord['longitude']}"

        category_data = request.data.pop("category")

        category_name = category_data["name"]
        if ec_qs := GoodsNServicesItemCategory.objects.filter(name=category_name):
            category_instance = ec_qs[0]
        else:
            image, icon = None, None

            if category_data.get("image"):
                image = category_data.pop("image")

            if category_data.get("icon"):
                icon = category_data.pop("icon")

            category_instance = GoodsNServicesItemCategory(
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
        
        category_data = request.data.pop("category")

        category_name = category_data["name"]
        if not (category_qs := GoodsNServicesItemCategory.objects.filter(name=category_name)):
            GoodsNServicesItemCategory.objects.create(name=category_name)
            category_qs = GoodsNServicesItemCategory.objects.filter(name=category_name)
        image, icon = None, None

        if category_data.get("image"):
            image = category_data.pop("image")

        if category_data.get("icon"):
            icon = category_data.pop("icon")

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


class IntegrationGoodsNServicesItemAPI(GoodsNServicesItemAPI):
    serializer_class = GoodsNServicesItemSerializerForIntegrationUser
