from rest_framework import serializers

from modules.ecology.models import File, FileType


class FileShortSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            "id",
            "link",
            "type",
            "name",
        ]

    def get_link(self, instance: File):
        return serializers.FileField().to_representation(instance.file)


class FileSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    type = serializers.ChoiceField(
        choices=[FileType.IMAGE, FileType.DOCUMENT], read_only=True
    )
    name = serializers.CharField(read_only=True)

    class Meta:
        model = File
        fields = [
            "id",
            "link",
            "type",
            "order",
            "name",
        ]
        ref_name = "ecology_file_serializer"

    def get_link(self, instance: File):
        return serializers.FileField().to_representation(instance.file)
