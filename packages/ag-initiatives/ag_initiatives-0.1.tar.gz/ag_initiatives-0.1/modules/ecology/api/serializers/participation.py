from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from config.settings import settings
from modules.core.models import User
from modules.ecology.api.serializers import EventListSerializer
from modules.ecology.api.serializers.excel import ExcelSerializer
from modules.ecology.models import ParticipationUserEvent
from modules.ecology.models.participation_user_event import ParticipationStatus


class ParticipationUserListSerializer(serializers.ModelSerializer):
    event = EventListSerializer()

    class Meta:
        model = ParticipationUserEvent
        fields = "__all__"


class ParticipationSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(source="event.id")
    event_name = serializers.CharField(source="event.name")
    event_address = serializers.CharField(source="event.address")
    event_start_date = serializers.CharField(source="event.start_date")
    event_expiry_date = serializers.CharField(source="event.expiry_date")
    event_start_time = serializers.CharField(source="event.start_time")
    event_expiry_time = serializers.CharField(source="event.expiry_time")
    description = serializers.CharField(source="event.description")
    reward = serializers.IntegerField(source="event.reward")
    participant_FIO = serializers.SerializerMethodField(
        method_name="get_participant_FIO"
    )

    class Meta:
        model = ParticipationUserEvent
        fields = (
            "event_id",
            "event_name",
            "event_address",
            "event_start_date",
            "event_expiry_date",
            "event_start_time",
            "event_expiry_time",
            "description",
            "participant_FIO",
            "reward",
            "status",
        )

    def get_participant_FIO(self, instance):
        participant: User = self.instance.participant
        if not participant:
            raise ValidationError("Участник не передан")
        return f"{participant.last_name} {participant.first_name} {participant.patronymic_name}"


class ParticipationListSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(source="event.id")
    event_name = serializers.CharField(source="event.name")
    locality = serializers.CharField(source="event.locality")
    operation_timestamp = serializers.DateTimeField(source="confirmation_timestamp")
    reward = serializers.IntegerField(source="event.reward")
    participant_FIO = serializers.SerializerMethodField(
        method_name="get_participant_FIO"
    )

    class Meta:
        model = ParticipationUserEvent
        fields = (
            "event_id",
            "event_name",
            "locality",
            "status",
            "operation_timestamp",
            "reward",
            "participant_FIO",
        )

    def get_participant_FIO(self, instance: ParticipationUserEvent):
        participant: User = instance.participant
        if not participant:
            raise ValidationError("Участник не передан")
        return f"{participant.last_name} {participant.first_name} {participant.patronymic_name}"


class ParticipationOrganizerExcelSerializer(ExcelSerializer):
    event_name = serializers.CharField(source="event.name")
    locality = serializers.CharField(source="event.locality")
    reward = serializers.IntegerField(source="event.reward")
    type = serializers.SerializerMethodField(method_name="get_type")
    participant_FIO = serializers.SerializerMethodField(
        method_name="get_participant_FIO"
    )
    operation_timestamp = serializers.SerializerMethodField(
        method_name="get_operation_timestamp"
    )

    HEADER_MAPPING = {
        "event_name": "Наименование предложения",
        "locality": "Муниципальное образование",
        "type": "Тип операции",
        "operation_timestamp": "Дата и время",
        "reward": "Количество бонусов",
        "participant_FIO": "ФИО Пользователя",
    }

    COLUMN_SIZES = 30
    FILE_NAME = "Organizer history"

    class Meta:
        model = ParticipationUserEvent
        fields = (
            "event_name",
            "locality",
            "type",
            "operation_timestamp",
            "reward",
            "participant_FIO",
        )

    def get_type(self, instance: ParticipationUserEvent):
        if instance.status == ParticipationStatus.CONFIRMED:
            return "Начисление"
        elif instance.status == ParticipationStatus.DECLINED:
            return "Отказ начисления"

    def get_operation_timestamp(self, instance: ParticipationUserEvent):
        try:
            time_zone = timezone.get_current_timezone() if settings.USE_TZ else None

            if not time_zone:
                date = instance.confirmation_timestamp.date()
                time = instance.confirmation_timestamp.time().strftime("%H:%M")
                return f"{date} {time}"

            date = instance.confirmation_timestamp.astimezone(time_zone).date()
            time = (
                instance.confirmation_timestamp.astimezone(time_zone)
                .time()
                .strftime("%H:%M")
            )
            return f"{date} {time}"
        except AttributeError:
            return None

    def get_participant_FIO(self, instance: ParticipationUserEvent):
        participant: User = instance.participant
        if not participant:
            raise ValidationError("Участник не передан")
        return f"{participant.last_name} {participant.first_name} {participant.patronymic_name}"
