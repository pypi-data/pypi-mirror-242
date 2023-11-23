from rest_framework import serializers

from modules.core.models import SettingsModule


class SettingsModuleSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели настройки модулей. """

    class Meta:
        model = SettingsModule
        fields = (
            "id",
            "type",
            "header",
            "text",
            "image",
            "video",
            "link_title",
            "link",
        )
