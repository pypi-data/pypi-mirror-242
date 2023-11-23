from rest_framework import serializers

from modules.appeals_pos.models.appeal import Coordinates


class CoordinatesSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def create(self, validated_data):
        return str(Coordinates(**validated_data))

    def to_representation(self, instance):
        [latitude, longitude] = str(instance).split(",")
        return {
            "latitude": latitude,
            "longitude": longitude,
        }

    class Meta:
        ref_name = 'file_pos_serializer'
