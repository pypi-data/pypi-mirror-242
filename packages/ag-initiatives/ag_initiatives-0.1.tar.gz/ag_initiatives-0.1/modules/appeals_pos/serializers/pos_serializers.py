from rest_framework import serializers


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    okato = serializers.CharField()
    coordinates = serializers.CharField()
