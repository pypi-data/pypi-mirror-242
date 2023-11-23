from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from modules.map_works.api.serializers import GeoJSONField
from modules.map_works.models import Location, Works


class LocationSerializer(serializers.ModelSerializer):
    work = serializers.PrimaryKeyRelatedField(
        queryset=Works.objects.all(),
        write_only=True,
        required=False,
    )
    gis_point = GeoJSONField(allow_null=True)
    gis_polygon = GeoJSONField(allow_null=True)

    class Meta:
        model = Location
        fields = [
            "id",
            "work",
            "address",
            "gis_point",
            "gis_polygon",
        ]


class LocationMapSerializer(GeoFeatureModelSerializer):
    id = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    state_label = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    works_id = serializers.SerializerMethodField()

    class Meta:
        model = Location
        geo_field = "gis_point"

        fields = [
            "id",
            "state",
            "state_label",
            "category",
            "works_id",
        ]

    def get_id(self, obj: Location):
        return obj.work.id

    def get_state(self, obj: Location):
        return obj.work.state

    def get_state_label(self, obj: Location):
        return obj.work.state_label

    def get_category(self, obj: Location):
        return obj.work.category.id

    def get_works_id(self, obj: Location):
        return obj.work.id
