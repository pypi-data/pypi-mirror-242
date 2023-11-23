from rest_framework import serializers

from modules.map_works.models import InstitutionType


class InstitutionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionType
        fields = "__all__"
