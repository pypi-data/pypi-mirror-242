from rest_framework import serializers

from modules.api.serializers import LocalityShortSerializer
from modules.api.serializers.organization import DepartmentAsOrganizationSerializer
from modules.ecology.api.serializers import GoodsNServicesItemCategorySerializer
from modules.ecology.api.serializers.coordinates import CoordinatesSerializer
from modules.ecology.models import GoodsNServicesItem


class GoodsNServicesItemListSerializer(serializers.ModelSerializer):
    category = GoodsNServicesItemCategorySerializer()
    locality = LocalityShortSerializer()
    display_localities = LocalityShortSerializer(many=True)

    class Meta:
        model = GoodsNServicesItem
        fields = [
            "id",
            "name",
            "description",
            "category",
            "locality",
            "start_date",
            "expiry_date",
            "start_time",
            "expiry_time",
            "cost",
            "address",
            "display_localities"
        ]


class GoodsNServicesItemDetailsSerializer(serializers.ModelSerializer):
    category = GoodsNServicesItemCategorySerializer()
    locality = LocalityShortSerializer()
    organization = DepartmentAsOrganizationSerializer()
    coordinates = CoordinatesSerializer(
        source="object_coordinates",
    )
    display_localities = LocalityShortSerializer(many=True)

    class Meta:
        model = GoodsNServicesItem
        fields = [
            "id",
            "name",
            "description",
            "locality",
            "category",
            "organization",
            "multiple_purchase",
            "maximum_purchasers",
            "address",
            "coordinates",
            "start_date",
            "expiry_date",
            "start_time",
            "expiry_time",
            "cost",
            "display_localities"
        ]


class GoodsNServicesItemFullDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsNServicesItem
        fields = "__all__"
