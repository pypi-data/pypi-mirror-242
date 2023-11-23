from rest_framework import serializers

from modules.initiatives.models import InitiativeFile, InitiativeFileType


class InitiativeFileShortSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeFile
        fields = [
            "id",
            "link",
            "type",
            "name",
        ]

    def get_link(self, instance: InitiativeFile):
        return serializers.FileField().to_representation(instance.file)


class InitiativeFileSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    type = serializers.ChoiceField(
        choices=[InitiativeFileType.IMAGE, InitiativeFileType.DOCUMENT], read_only=True
    )
    name = serializers.CharField(read_only=True)

    class Meta:
        model = InitiativeFile
        fields = [
            "id",
            "link",
            "type",
            "order",
            "name",
        ]

    def get_link(self, instance: InitiativeFile):
        return serializers.FileField().to_representation(instance.file)
