from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from modules.core.models import Locality
from modules.initiatives.models import InitiativeAcceptingSettings


class InitiativeSettingsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitiativeAcceptingSettings
        fields = (
            "locality",
            "category",
            "duration_month",
            "votes_threshold",
            "active",
            "type",
        )

    def validate_votes_threshold(self, threshold):
        if threshold <= 0:
            raise ValidationError("Значение должно быть больше нуля.")
        return threshold

    def validate_duration_month(self, duration):
        if duration <= 0:
            raise ValidationError("Значение должно быть больше нуля.")
        return duration

    def validate(self, data):
        localities = data.get("locality", None).copy()
        type = data.get("type", None)
        existing_settings = InitiativeAcceptingSettings.objects.filter(
            locality__in=data.get("locality", None),
            category_id=data.get("category", None),
        ).exclude(id=self.instance.id if self.instance else None)
        if existing_settings:
            raise ValidationError("Приём инициатив по данным параметрам уже настроен")
        if type:
            if type == "REGIONAL":
                if existing_settings:
                    raise ValidationError("Приём инициатив по данным параметрам уже настроен")
            else:

                exists_locality = list(InitiativeAcceptingSettings.objects.filter(
                    type=data.get("type", None),
                    category_id=data.get("category", None),
                ).values_list("locality__id", flat=True))

                for locality in data.get("locality", None):
                    if locality.id not in exists_locality:
                        localities.remove(locality)

                if localities:
                    localities = [locality.name for locality in localities]
                    raise ValidationError(
                        f"Приём инициатив по данным параметрам для данных МО уже настроен:  {', '.join(localities)}.")
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        department = user.sub_permissions.operator_permissions.department
        validated_data["department"] = department
        localities = validated_data.pop('locality')
        obj = self.Meta.model.objects.create(**validated_data)
        # if obj.type == "REGIONAL":
        #     localities = Locality.objects.all()
        obj.locality.set(localities)
        return obj

    def update(self, instance, validated_data):
        # if validated_data['type'] == 'REGIONAL':
        #     validated_data.pop('locality')
        return super(InitiativeSettingsWriteSerializer, self).update(
            instance, validated_data)
