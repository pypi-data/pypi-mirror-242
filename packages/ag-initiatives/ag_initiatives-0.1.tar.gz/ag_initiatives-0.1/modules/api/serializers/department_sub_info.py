from rest_framework import serializers

from modules.core.models import LkoLevel, LkoType


class LkoLevelSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели уровня ЛКО. """

    class Meta:
        model = LkoLevel
        fields = (
            "id",
            "name",
        )


class LkoTypeSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели типа Лко. """

    class Meta:
        model = LkoType
        fields = (
            "id",
            "name",
        )
