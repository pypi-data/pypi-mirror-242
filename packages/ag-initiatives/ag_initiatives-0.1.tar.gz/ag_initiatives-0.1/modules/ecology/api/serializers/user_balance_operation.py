from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from config.settings import settings
from modules.core.models import User
from modules.ecology.api.serializers.excel import ExcelSerializer
from modules.ecology.models import UserBalanceOperation, UserBalanceOperationType


class UserBalanceOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalanceOperation
        fields = "__all__"


class PartnerHistorySerializer(serializers.ModelSerializer):
    reward_id = serializers.IntegerField(source="purchase.goods_n_services_item.id")
    reward_name = serializers.CharField(source="purchase.goods_n_services_item.name")
    locality = serializers.CharField(source="purchase.goods_n_services_item.locality")
    user_FIO = serializers.SerializerMethodField(method_name="get_user_FIO")

    class Meta:
        model = UserBalanceOperation
        fields = (
            "reward_id",
            "reward_name",
            "type",
            "locality",
            "timestamp",
            "amount",
            "user_FIO",
        )

    def get_user_FIO(self, instance):
        user: User = instance.user
        if not user:
            raise ValidationError("Участник не передан")
        return f"{user.last_name} {user.first_name} {user.patronymic_name}"


class PartnerHistoryExcelSerializer(ExcelSerializer):
    reward_name = serializers.CharField(source="purchase.goods_n_services_item.name")
    locality = serializers.CharField(source="purchase.goods_n_services_item.locality")
    user_FIO = serializers.SerializerMethodField(method_name="get_user_FIO")
    type = serializers.SerializerMethodField(method_name="get_type")
    timestamp = serializers.SerializerMethodField(method_name="get_timestamp")

    HEADER_MAPPING = {
        "reward_name": "Наименование поощрения",
        "type": "Тип операции",
        "locality": "Муниципальное образование",
        "timestamp": "Дата и время",
        "amount": "Количество бонусов",
        "user_FIO": "ФИО Пользователя",
    }

    COLUMN_SIZES = 30

    SHEET_NAME = "sheet1"
    FILE_NAME = "Partner history"

    class Meta:
        model = UserBalanceOperation
        fields = ("reward_name", "type", "locality", "timestamp", "amount", "user_FIO")

    def get_type(self, instance: UserBalanceOperation):
        if instance.type == UserBalanceOperationType.INCOME:
            return "Возврат"
        return UserBalanceOperationType.RESOLVER[UserBalanceOperationType.EXPENSE]

    def get_timestamp(self, instance: UserBalanceOperation):
        try:
            time_zone = timezone.get_current_timezone() if settings.USE_TZ else None

            if not time_zone:
                date = instance.timestamp.date()
                time = instance.timestamp.time().strftime("%H:%M")
                return f"{date} {time}"

            date = instance.timestamp.astimezone(time_zone).date()
            time = instance.timestamp.astimezone(time_zone).time().strftime("%H:%M")
            return f"{date} {time}"
        except AttributeError:
            return None

    def get_user_FIO(self, instance):
        user: User = instance.user
        if not user:
            raise ValidationError("Участник не передан")
        return f"{user.last_name} {user.first_name} {user.patronymic_name}"
