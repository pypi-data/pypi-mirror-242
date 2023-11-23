from rest_framework import serializers

from modules.api.serializers.image import ImageSerializer
from modules.api.serializers.video import VideoDetailReadSerializer
from modules.core.models import ProjectInfo
from modules.core.models.project_info import BlockFile, BlockLink
import os


class BlockFileSerializer(serializers.ModelSerializer):
    file_size = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = BlockFile
        fields = '__all__'

    @staticmethod
    def get_file_size(obj):
        url = obj.file.name
        if url and obj.file.storage.exists(url):
            return obj.file.size
        return None

    @staticmethod
    def get_file_url(obj):
        return obj.file.url if obj.file.name else None

    @staticmethod
    def get_file_name(obj):
        return os.path.basename(obj.file.name)

    def to_representation(self, value):
        to_representation = super().to_representation(value)
        to_representation['file'] = to_representation.pop('file_url')
        return to_representation


class BlockLinkSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    class Meta:
        model = BlockLink
        fields = '__all__'

    @staticmethod
    def get_name(obj):
        return obj.name if obj.name else None

    @staticmethod
    def get_link(obj):
        return obj.link if obj.link else None


class ProjectInfoSerializer(serializers.ModelSerializer):
    video = VideoDetailReadSerializer()
    image = ImageSerializer()
    files = BlockFileSerializer(many=True)
    links = BlockLinkSerializer(many=True)

    class Meta:
        model = ProjectInfo
        fields = (
            "block_id",
            "text",
            "video",
            "image",
            "files_name",
            "files",
            "links",
        )
