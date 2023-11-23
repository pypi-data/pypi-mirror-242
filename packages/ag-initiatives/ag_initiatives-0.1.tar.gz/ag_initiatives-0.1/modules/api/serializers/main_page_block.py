from rest_framework import serializers

from modules.core.models import MainPageBlock


class MainPageBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainPageBlock
        fields = ["id", "name", "order"]
