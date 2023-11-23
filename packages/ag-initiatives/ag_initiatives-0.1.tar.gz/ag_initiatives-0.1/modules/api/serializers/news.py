from rest_framework import serializers

from modules.api.serializers import CategorySerializer
from modules.api.serializers.audio import AudioSerializer
from modules.api.serializers.video import VideoDetailReadSerializer
from modules.core.models import News


class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    video = VideoDetailReadSerializer()
    audio = AudioSerializer()

    class Meta:
        model = News
        fields = "__all__"


class NewsShortSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    video = VideoDetailReadSerializer()
    audio = AudioSerializer()

    class Meta:
        model = News
        exclude = ["text"]


class NewsCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    video_id = serializers.IntegerField(
        required=False, allow_null=True,
    )
    audio_id = serializers.IntegerField(
        required=False, allow_null=True,
    )
    image = serializers.ImageField(
        required=False, allow_null=True,
    )

    class Meta:
        model = News
        fields = [
            "title",
            "description",
            "category_id",
            "video_id",
            "audio_id",
            "text",
            "url",
            "url_title",
            "image",
            "is_public",
        ]

    def create(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance: News, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.category_id = validated_data.get("category_id", instance.category_id)
        instance.video_id = validated_data.get("video_id", instance.video_id)
        instance.audio_id = validated_data.get("audio_id", instance.audio_id)
        instance.text = validated_data.get("text", instance.text)
        instance.url = validated_data.get("url", instance.url)
        instance.url_title = validated_data.get("url_title", instance.url_title)
        instance.image = validated_data.get("image", instance.image)
        instance.is_public = validated_data.get("is_public", instance.is_public)

        instance.save()
        return instance
