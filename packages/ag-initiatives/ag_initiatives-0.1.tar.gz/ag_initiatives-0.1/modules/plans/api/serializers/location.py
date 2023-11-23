from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from modules.plans.api.serializers import GeoJSONField
from modules.plans.models import Location, Plan


class LocationSerializer(serializers.ModelSerializer):
    gis_point = GeoJSONField(allow_null=True)
    gis_polygon = GeoJSONField(allow_null=True)

    class Meta:
        model = Location
        fields = [
            "address",
            "gis_point",
            "gis_polygon",
        ]
        ref_name = 'plans_location_serializer'


class LocationMapSerializer(GeoFeatureModelSerializer):
    category = serializers.SerializerMethodField()
    plan_id = serializers.SerializerMethodField()

    class Meta:
        model = Location
        geo_field = "gis_point"

        fields = [
            "id",
            "category",
            "plan_id",
        ]

    def get_category(self, obj: Location):
        return obj.plan.category.id

    def get_plan_id(self, obj: Location):
        return obj.plan.id
