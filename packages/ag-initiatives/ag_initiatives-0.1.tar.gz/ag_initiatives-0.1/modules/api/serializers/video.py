from rest_framework import serializers

from modules.core.models import Video


class VideoDetailReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"
