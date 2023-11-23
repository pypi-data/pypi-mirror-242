from typing import Dict

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from config import settings
from modules.api.serializers import LocalityShortSerializer
from modules.appeals_pos.models import Appeal
from modules.appeals_pos.models.appeal import AppealState
from modules.appeals_pos.models.subcategory import Subcategory
from modules.appeals_pos.serializers.appeal_state_change import (
    AppealStateChangeSerializer,
)
from modules.appeals_pos.serializers.category import SubcategoryFullSerializer
from modules.appeals_pos.serializers.coordinates import CoordinatesSerializer
from modules.appeals_pos.serializers.file import FileSerializer
from modules.core.models import User
from modules.ecology.api.serializers.excel import ExcelSerializer


class AppealSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True, source="user.id")
    creation_date_time = serializers.DateTimeField(read_only=True)
    files = FileSerializer(many=True, required=False)
    subcategory = SubcategoryFullSerializer(read_only=True)
    coordinates = CoordinatesSerializer(
        source="object_coordinates",
        required=False, allow_null=True,
    )
    locality = LocalityShortSerializer()
    status = serializers.SerializerMethodField(method_name="get_status_name")

    class Meta:
        model = Appeal
        fields = "__all__"

    def get_status_name(self, instance: Appeal):
        return AppealState.RESOLVER.get(instance.status)


class AppealShortSerializer(serializers.ModelSerializer):
    subcategory = SubcategoryFullSerializer(read_only=True)
    status_name = serializers.SerializerMethodField()

    class Meta:
        model = Appeal
        fields = [
            "id",
            "pos_id",
            "status",
            "status_name",
            "subcategory",
            "to_publish",
        ]

    def get_status_name(self, instance: Appeal):
        return AppealState.RESOLVER.get(instance.status)


class AppealFullSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source="user.first_name")
    author_last_name = serializers.CharField(source="user.last_name")
    author_patronymic_name = serializers.CharField(source="user.patronymic_name")
    creation_date_time = serializers.DateTimeField()
    files = FileSerializer(many=True, required=False)
    subcategory = SubcategoryFullSerializer()
    history = serializers.SerializerMethodField()
    coordinates = CoordinatesSerializer(
        source="object_coordinates",
        required=False, allow_null=True,
    )
    locality = LocalityShortSerializer()
    status_name = serializers.SerializerMethodField()

    class Meta:
        model = Appeal
        fields = "__all__"

    def get_history(self, instance: Appeal):
        history = instance.history.order_by("-created_at")
        return AppealStateChangeSerializer(history, many=True).data

    def get_status_name(self, instance: Appeal):
        return AppealState.RESOLVER.get(instance.status)


class AppealWriteSerializer(serializers.ModelSerializer):
    subcategory_id = serializers.IntegerField()
    coordinates = CoordinatesSerializer(required=False, allow_null=True)
    # key: Имя поля для проверки, value: Сообщение об ошибке
    _validation_config: Dict[str, str] = {
        "first_name": "имя",
        "last_name": "фамилия",
        "birth_date": "дата рождения",
        "email": "адрес электронной почты",
        "phone": "контактный телефон",
        "residential_locality": "муниципальное образование регистрации",
        "registration_locality": "муниципальное образование проживания",
        "snils": "номер СНИЛС",
    }

    class Meta:
        model = Appeal
        fields = [
            "id",
            "text",
            "subcategory_id",
            "coordinates",
            "address",
            "files",
            "to_publish",
        ]

    def create(self, validated_data) -> Appeal:
        user: User = self.context["request"].user
        coordinates_data = validated_data.pop("coordinates", None)
        subcategory_id = validated_data.pop("subcategory_id")
        files = validated_data.pop("files", None)

        coordinates = None
        if coordinates_data:
            coordinates_serializer = CoordinatesSerializer(data=coordinates_data)
            coordinates_serializer.is_valid(raise_exception=True)
            coordinates = coordinates_serializer.save()

        try:
            Subcategory.objects.get(pk=subcategory_id)
        except Subcategory.DoesNotExist:
            raise ValidationError("Подкатегория не найдена")

        instance = Appeal(
            user=user,
            creation_date_time=timezone.now(),
            coordinates=coordinates,
            locality=user.residential_locality,
            subcategory_id=subcategory_id,
            **validated_data,
        )
        instance.save()

        if files:
            instance.files.set(files)

        return instance

    def validate(self, attrs):
        user: User = self.context["request"].user
        if not user.esia_verified:
            raise ValidationError(
                {"detail": "Для направления обращения Вам необходимо подтвердить учетную запись портала Госуслуг."
                           " Информацию о способах подтверждения учетной записи Вы можете получить на портале Госуслуг:"
                           " https://www.gosuslugi.ru/"})

        error_messages = []
        for user_attr, error_message in self._validation_config.items():
            if not getattr(user, user_attr):
                error_messages.append(error_message)

        if error_messages:
            raise ValidationError({"detail": f"В Вашем личном кабинете портала «Активный гражданин» отсутствует "
                                             f"{', '.join([msg for msg in error_messages])} пользователя. Внесите данные в личном кабинете портала"
                                             f" Госуслуг: https://www.gosuslugi.ru/ и авторизуйтесь на портале"
                                             f" «Активный гражданин»: https://24ag.ru/ повторно."})
        return attrs


class AppealExcelSerializer(ExcelSerializer):
    COLUMN_SIZES = 40
    HEADER_MAPPING = {
        "pos_id": "Идентификатор ПОС",
        "created_datetime": "Дата и время создания",
        "user_first_name": "Имя заявителя",
        "user_last_name": "Фамилия заявителя",
        "user_patronymic_name": "Отчество заявителя",
        "user_email": "Email заявителя",
        "user_phone": "Телефон заявителя",
        "category": "Категория обращения",
        "subcategory": "Подкатегория обращения",
        "text": "Текст обращения",
        "address": "Адрес, по которому подано обращение",
        "to_publish": "Тип публикации обращения",
        "status": "Текущий статус обращения",
        "answer": "Ответ на обращение",
    }

    created_datetime = serializers.SerializerMethodField()
    user_first_name = serializers.SerializerMethodField()
    user_last_name = serializers.SerializerMethodField()
    user_patronymic_name = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    user_phone = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    text = serializers.CharField()
    address = serializers.CharField()
    to_publish = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Appeal
        fields = [
            "pos_id",
            "created_datetime",
            "user_first_name",
            "user_last_name",
            "user_patronymic_name",
            "user_email",
            "user_phone",
            "category",
            "subcategory",
            "text",
            "address",
            "to_publish",
            "status",
            "answer",
        ]

    def get_created_datetime(self, instance: Appeal):
        try:
            time_zone = timezone.get_current_timezone() if settings.USE_TZ else None

            if not time_zone:
                date = instance.creation_date_time.date()
                time = instance.creation_date_time.time().strftime("%H:%M")
                return f"{date} {time}"

            date = instance.creation_date_time.astimezone(time_zone).date()
            time = (
                instance.creation_date_time.astimezone(time_zone)
                .time()
                .strftime("%H:%M")
            )
            return f"{date} {time}"
        except AttributeError:
            return None

    def get_user_first_name(self, instance: Appeal):
        return instance.user.first_name if instance.user.first_name else ""

    def get_user_last_name(self, instance: Appeal):
        return instance.user.last_name if instance.user.last_name else ""

    def get_user_patronymic_name(self, instance: Appeal):
        return instance.user.patronymic_name if instance.user.patronymic_name else ""

    def get_user_email(self, instance: Appeal):
        return instance.user.email if instance.user.email else ""

    def get_user_phone(self, instance: Appeal):
        return instance.user.phone if instance.user.phone else ""

    def get_category(self, instance: Appeal):
        return instance.subcategory.category.name

    def get_subcategory(self, instance: Appeal):
        return instance.subcategory.name

    def get_to_publish(self, instance: Appeal):
        if instance.to_publish:
            return "Публичное"
        return "Приватное"

    def get_status(self, instance: Appeal):
        return AppealState.RESOLVER.get(instance.status)

    def get_answer(self, instance: Appeal):
        if instance.status not in [
            AppealState.RESPONDED,
            AppealState.MODERATION_REJECTED,
        ]:
            return ""
        appeal_state_change_with_answer = instance.history.filter(
            answer__isnull=False
        ).first()
        return (
            appeal_state_change_with_answer.answer
            if appeal_state_change_with_answer
            else ""
        )
