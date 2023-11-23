from rest_framework import serializers

from modules.ecology.models import GoodsNServicesItemCategory


class GoodsNServicesItemCategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsNServicesItemCategory
        fields = [
            "id",
            "name",
            "color",
            "image",
            "icon",
        ]


class GoodsNServicesItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsNServicesItemCategory
        fields = "__all__"
