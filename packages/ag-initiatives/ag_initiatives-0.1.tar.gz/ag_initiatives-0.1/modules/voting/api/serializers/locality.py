from rest_framework import serializers

from modules.core.models import Locality, Municipality
from modules.voting.api.serializers import GeoJSONField


class LocalityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locality
        fields = [
            "id",
            "name",
            "type_short_name",
        ]


class MunicipalityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = [
            "id",
            "name",
            # "type_short_name",
        ]


class LocalityDetailsSerializer(serializers.ModelSerializer):
    gis_center = GeoJSONField()
    gis_border = GeoJSONField()

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
