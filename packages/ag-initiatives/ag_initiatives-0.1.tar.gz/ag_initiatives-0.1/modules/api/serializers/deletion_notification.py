from rest_framework import serializers

from modules.core.models import DeletionNotification


class DeletionNotificationSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели оповещения об удалении учётной записи. """

    class Meta:
        model = DeletionNotification
        fields = ("id", "header", "text")
