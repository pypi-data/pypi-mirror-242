import json
from rest_framework import serializers

from modules.core.models.locality import Locality


class LocalityIntegrationSerializer(serializers.ModelSerializer):
    gis_center = serializers.SerializerMethodField(method_name="get_gis_center")

    class Meta:
        model = Locality
        fields = [
            "id",
            "parent",
            "name",
            "type",
            "type_short_name",
            "gis_center",
        ]

    def get_gis_center(self, model: Locality):
        if model.gis_center is None:
            return None
        return json.loads(model.gis_center.geojson)

class LocalityIntegrationShortSerializer(serializers.ModelSerializer):
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

