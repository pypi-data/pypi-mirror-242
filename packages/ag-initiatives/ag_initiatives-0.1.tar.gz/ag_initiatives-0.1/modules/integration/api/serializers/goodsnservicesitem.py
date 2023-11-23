from django.db.models import Q
from rest_framework import serializers

from config.settings import DOMAIN_NAME, MEDIA_URL
from modules.api.serializers.organization import DepartmentAsOrganizationSerializer
from modules.core.models.locality import Locality
from modules.ecology.models import (GoodsNServicesItem,
                                    GoodsNServicesItemCategory, UserPurchase)
from modules.ecology.models.user_purchase import PurchaseStatus
from modules.integration.api.serializers.locality import (
    LocalityIntegrationSerializer, LocalityIntegrationShortSerializer)


class GoodsNServicesItemCategoryIntegrationSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = GoodsNServicesItemCategory
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


class GoodsNServicesItemSerializer(serializers.ModelSerializer):
    category = GoodsNServicesItemCategoryIntegrationSerializer()
    organization = DepartmentAsOrganizationSerializer()
    coordinates = serializers.SerializerMethodField()
    locality = LocalityIntegrationSerializer()
    display_localities = LocalityIntegrationShortSerializer(many=True)
    user_has_reward = serializers.BooleanField(required=False)
    url = serializers.SerializerMethodField()

    class Meta:
        model = GoodsNServicesItem
        fields = [
            "id",
            "url",
            "name",
            "category",
            "organization",
            "locality",
            "cost",
            "contacts",
            "description",
            "multiple_purchase",
            "maximum_purchasers",
            "start_date",
            "expiry_date",
            "start_time",
            "expiry_time",
            "address",
            "coordinates",
            "is_published",
            "contacts",
            "start_publication_date",
            "expiry_publication_date",
            "return_possibility",
            "display_localities",
            "user_has_reward",
        ]

    @staticmethod
    def get_url(obj):
        return f"{DOMAIN_NAME}/bonus/details/bonus/{obj.id}"

    @staticmethod
    def get_coordinates(obj):
        cord = obj.coordinates.split(", ") if obj.coordinates else [None, None]
        return {
            "latitude": cord[0],
            "longitude": cord[1],
        }


class GoodsNServicesItemSerializerForIntegrationUser(GoodsNServicesItemSerializer):
    status = serializers.SerializerMethodField()
    maximum_purchase_usage = serializers.SerializerMethodField()

    class Meta:
        model = GoodsNServicesItem
        fields = [
            "id",
            "url",
            "name",
            "category",
            "organization",
            "locality",
            "cost",
            "contacts",
            "description",
            "multiple_purchase",
            "maximum_purchasers",
            "maximum_purchase_usage",
            "start_date",
            "expiry_date",
            "start_time",
            "expiry_time",
            "address",
            "coordinates",
            "is_published",
            "contacts",
            "start_publication_date",
            "expiry_publication_date",
            "return_possibility",
            "display_localities",
            "user_has_reward",
            "status",
        ]

    def get_status(self, obj: GoodsNServicesItem):
        request = self.context.get('request')
        purchases = UserPurchase.objects.filter(goods_n_services_item=obj, user=request.user)
        if not purchases.exists():
            return []
        return [
            {
                'id': purchase.id,
                'status': purchase.status
            }
            for purchase in purchases]

    @staticmethod
    def get_maximum_purchase_usage(obj: GoodsNServicesItem) -> bool:
        if not obj.maximum_purchasers:
            return False
        return obj.maximum_purchasers <= UserPurchase.objects.filter(
            Q(goods_n_services_item=obj) & ~Q(status=PurchaseStatus.RETURNED)).count()


class GoodsNServicesItemCreateSerializer(serializers.ModelSerializer):
    display_localities = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Locality.objects.all(), required=False
    )

    class Meta:
        model = GoodsNServicesItem
        fields = [
            "name",
            "category",
            "organization",
            "locality",
            "cost",
            "contacts",
            "description",
            "multiple_purchase",
            "maximum_purchasers",
            "start_date",
            "expiry_date",
            "start_time",
            "expiry_time",
            "address",
            "coordinates",
            "is_published",
            "contacts",
            "start_publication_date",
            "expiry_publication_date",
            "return_possibility",
            "display_localities",
        ]

    @staticmethod
    def get_coordinates(obj):
        cord = obj.coordinates.split(", ") if obj.coordinates else [None, None]
        return {
            "latitude": cord[0],
            "longitude": cord[1],
        }
