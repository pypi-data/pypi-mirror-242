from rest_framework import serializers

from modules.appeals_pos.models.file import FileType, File


class FileSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField()
    file = serializers.FileField(write_only=True)

    class Meta:
        ref_name = 'file_pos_serializer'
        model = File
        fields = [
            "id",
            "smev_adapter_id",
            "file",
            "link",
            "name",
            "owner",
            "type",
        ]

    @staticmethod
    def get_link(obj: File):
        return obj.file.url if obj.file.name else None

    def create(self, validated_data):
        file = validated_data.get('file')
        file_name = validated_data.get('name')
        file_type = (
            FileType.IMAGE
            if file.content_type in ["image/png", "image/jpeg"]
            else FileType.DOCUMENT
        )
        file_instance = File.objects.create(
            file=file, name=file_name, type=file_type, owner=self.context['request'].user
        )
        return file_instance