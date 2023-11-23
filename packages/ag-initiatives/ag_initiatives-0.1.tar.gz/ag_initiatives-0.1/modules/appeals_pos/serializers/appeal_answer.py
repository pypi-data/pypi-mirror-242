from rest_framework import serializers

from modules.appeals_pos.models import AppealAnswer, AppealAttachment


class AppealAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    type = serializers.CharField()

    class Meta:
        model = AppealAttachment
        fields = ("file_name", "type", "file")

    @staticmethod
    def get_file(obj):
        return obj.file.url if obj.file.name else None


class AppealAnswerSerializer(serializers.ModelSerializer):
    answer_type_name = serializers.CharField()
    attachments = AppealAttachmentSerializer(many=True)

    class Meta:
        model = AppealAnswer
        exclude = ["files"]
