from django.core.files import File
from rest_framework import serializers

from modules.core.models import RoleInstruction, InstructionFile


class InstructionFileSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField(read_only=True)
    filename = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InstructionFile
        fields = (
            "link",
            "filename"
        )

    def get_link(self, instance: File):
        return serializers.FileField().to_representation(instance.file)

    def get_filename(self, instance: InstructionFile) -> str:
        return instance.file.name


class RoleInstructionSerializer(serializers.ModelSerializer):
    instructions = InstructionFileSerializer(many=True, required=False)

    class Meta:
        model = RoleInstruction
        fields = [
            "id",
            "role",
            "instructions",
        ]
