from rest_framework import serializers

from modules.map_works.models import WorkCategory


class WorkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCategory
        fields = "__all__"


class WorkCategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCategory
        fields = ["id", "name"]
