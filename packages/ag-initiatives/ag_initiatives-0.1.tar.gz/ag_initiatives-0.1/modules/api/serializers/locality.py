from rest_framework import serializers
from rest_framework.utils import json

from modules.core.models import Locality, Municipality, LocalityType


class LocalityShortSerializer(serializers.ModelSerializer):
    gis_center = serializers.SerializerMethodField(method_name="get_gis_center")

    class Meta:
        model = Locality
        fields = [
            "id",
            "name",
            "type_short_name",
            "gis_center"
        ]

    def get_gis_center(self, model: Locality):
        if model.gis_center is None:
            return None
        return json.loads(model.gis_center.geojson)


class LocalitySerializer(serializers.ModelSerializer):
    gis_center = serializers.SerializerMethodField(method_name="get_gis_center")
    gis_border = serializers.SerializerMethodField(method_name="get_gis_border")

    class Meta:
        model = Locality
        fields = [
            "id",
            "parent",
            "name",
            "type",
            "type_short_name",
            "gis_center",
            "gis_border",
        ]

    def get_gis_center(self, model: Locality):
        if model.gis_center is None:
            return None
        return json.loads(model.gis_center.geojson)

    def get_gis_border(self, model: Locality):
        if model.gis_border is None:
            return None
        return json.loads(model.gis_border.geojson)


class MunicipalityTreeSerializer(serializers.ModelSerializer):
    localities = LocalityShortSerializer(many=True)

    class Meta:
        model = Locality
        fields = [
            "id",
            "name",
            "type_short_name",
            "localities",
        ]


class MunicipalityWithUnavailableTreeSerializer(MunicipalityTreeSerializer):
    localities = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Locality
        fields = MunicipalityTreeSerializer.Meta.fields + [
            "is_available"
        ]

    def get_is_available(self, instance: Municipality):
        if hasattr(instance, "is_available"):
            return instance.is_available
        return True

    def get_localities(self, instance: Municipality):
        return None
        # if hasattr(instance, "allowed_localities"):
        #     return LocalityShortSerializer(instance.allowed_localities, many=True).data
        #
        # return LocalityShortSerializer(instance.localities.all(), many=True).data


class LocalityWithParentSerializer(LocalityShortSerializer):
    parent = LocalityShortSerializer()

    class Meta:
        model = Locality
        fields = LocalityShortSerializer.Meta.fields + ["parent"]


class LocalityTypeSerializer(serializers.ModelSerializer):
    """ Сериализатор для типов населённых пунктов и МО. """
    class Meta:
        model = LocalityType
        fields = (
            "id",
            "name",
        )