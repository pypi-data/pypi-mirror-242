from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from modules.api.serializers import (
    DepartmentShortSerializer,
    LocalityShortSerializer,
    InitiativeCategoryDetailedSerializer,
)
from modules.core.models import Locality
from modules.initiatives.models import InitiativeAcceptingSettings


class InitiativeAcceptingSettingsSerializer(serializers.ModelSerializer):
    department = DepartmentShortSerializer()
    locality = LocalityShortSerializer(many=True)
    category = InitiativeCategoryDetailedSerializer()
    localities = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeAcceptingSettings
        exclude = ('type',)

    def get_localities(self, instance: InitiativeAcceptingSettings):
        localities = set(
            instance.locality.filter(parent__isnull=False).values_list(
                "name", flat=True
            )
        ) | set(
            instance.locality.filter(parent__isnull=True).values_list(
                "localities__name", flat=True
            )
        )
        localities.discard(None)
        return localities


class InitiativeAcceptingSettingsWriteSerializer(serializers.ModelSerializer):
    locality = LocalityShortSerializer(many=True)

    class Meta:
        model = InitiativeAcceptingSettings
        fields = (
            "locality",
            "category",
            "duration_month",
            "votes_threshold",
            "active",
        )

    def validate_votes_threshold(self, threshold):
        if threshold <= 0:
            raise ValidationError("Значение должно быть больше нуля.")
        return threshold

    def validate_duration_month(self, duration):
        if duration <= 0:
            raise ValidationError("Значение должно быть больше нуля.")
        return duration

    def validate_locality(self, locality: dict):
        locality_instance = Locality.objects.filter(name=locality.get("name")).first()
        department = getattr(self.context["request"].user, "department", None)
        if locality_instance and locality_instance in department.locality.all():
            return locality_instance
        raise ValidationError(
            detail="Невозможно открыть прием инициатив по выбранному муниципальному образованию. "
            "Обратитесь к Оператору системы для добавления муниципального образования в "
            "профиль вашего ведомства",
            code=400,
        )

    def create(self, validated_data):
        validated_data["department"] = self.context["request"].user.department
        obj = self.Meta.model.objects.create(**validated_data)
        return obj
