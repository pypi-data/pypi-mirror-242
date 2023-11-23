from django.utils.safestring import mark_safe
from rest_framework import serializers

from modules.core.models import InformationalMessages


class HTMLLineBreakField(serializers.Field):
    def to_representation(self, value):
        return mark_safe(value.replace('\r\n', '<br>'))


class InformationalMessagesSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели информационных сообщений. """
    text = HTMLLineBreakField()

    class Meta:
        model = InformationalMessages
        fields = (
            "header",
            "text",
            "image",
            "link_title",
            "link"
        )
