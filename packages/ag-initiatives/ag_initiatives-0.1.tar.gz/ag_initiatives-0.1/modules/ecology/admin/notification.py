from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from config.settings import settings
from modules.core.models import User
from modules.ecology.api.serializers.excel import ExcelSerializer
from modules.ecology.models import (
    Notification,
    NotificationType,
    UserBalanceOperationType,
)


class NotificationExcelSerializer(ExcelSerializer):
    """Сериализатор для выгрузки в ексель, классная штука кстати, можно пользоваться"""

    user_fio = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    operation_type = serializers.SerializerMethodField()
    operation_object = serializers.SerializerMethodField()
    operation_object_name = serializers.SerializerMethodField()

    SHEET_NAME = "operations"
    FILE_NAME = "Report operations"

    HEADER_MAPPING = {
        "user_fio": "ФИО пользователя",
        "timestamp": "Дата-время",
        "operation_type": "Тип операции",
        "operation_object": "Объект операции",
        "operation_object_name": "Наименование объекта операции",
    }

    COLUMN_SIZES = 30

    class Meta:
        model = Notification
        fields = [
            "user_fio",
            "timestamp",
            "operation_type",
            "operation_object",
            "operation_object_name",
        ]

    def get_user_fio(self, instance: Notification):
        user: User = instance.user
        return f"{user.last_name} {user.first_name} {user.patronymic_name}"

    def get_timestamp(self, instance: Notification):
        try:
            time_zone = timezone.get_current_timezone() if settings.USE_TZ else None

            if not time_zone:
                date = instance.timestamp.date()
                time = instance.timestamp.time().strftime("%H%M")
                return f"{date} {time}"

            date = instance.timestamp.astimezone(time_zone).date()
            time = instance.timestamp.astimezone(time_zone).time().strftime("%H:%M")
            return f"{date} {time}"
        except AttributeError:
            return None

    def get_operation_type(self, instance: Notification):
        if not instance.user_balance_operation:
            return None
        if instance.type == NotificationType.RETURN_GOODSNSERVICES_PURCHASE:
            return "Возврат"

        return UserBalanceOperationType.RESOLVER[instance.user_balance_operation.type]

    def get_operation_object(self, instance: Notification):
        return NotificationType.RESOLVER[instance.type]

    def get_operation_object_name(self, instance: Notification):
        try:
            if (
                instance.type == NotificationType.EVENT_PARTICIPATION
                or instance.type == NotificationType.DECLINE_EVENT_PARTICIPATION
            ):
                return instance.participation.event.name
            elif (
                instance.type == NotificationType.GOODSNSERVICES_PURCHASE
                or instance.type == NotificationType.RETURN_GOODSNSERVICES_PURCHASE
            ):
                return instance.user_purchase.goods_n_services_item.name
            elif instance.type == NotificationType.VOTING_PARTICIPATION:
                return instance.vote.name
            elif (
                instance.type == NotificationType.ADDING_INITIATIVE
                or instance.type == NotificationType.APPROVE_INITIATIVE
            ):
                return instance.initiative.title
            return None
        except AttributeError:
            return None


def notification_report(modeladmin, request, queryset):
    """Действие в админке на выгрузку в эксель"""
    if queryset.count() == 0:
        return

    data = NotificationExcelSerializer(queryset, many=True).data
    response = NotificationExcelSerializer.excel_response(data, response_status=200)
    return response


notification_report.short_description = "Отчет по операциям"


class OperationObjectListFilter(SimpleListFilter):
    """Костыльный фильтр по типу уведомлений, переименованный в объект операции"""

    title = "Объект операции"
    parameter_name = "operation_object"

    def lookups(self, request, model_admin):
        return NotificationType.RESOLVER.items()

    def queryset(self, request, queryset):
        if self.value():
            return Notification.objects.filter(type=self.value())
        return queryset


class OperationTypeListFilter(SimpleListFilter):
    """Костыльный фильтр по типу операции, который фильтрует еще и по несуществующему в базе возврату :)"""

    title = "Тип операции"
    parameter_name = "operation_type"

    def lookups(self, request, model_admin):
        return ("INCOME", "Зачисление"), ("EXPENSE", "Списание"), ("RETURN", "Возврат")

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == "RETURN":
                return Notification.objects.filter(
                    type=NotificationType.RETURN_GOODSNSERVICES_PURCHASE
                )
            return Notification.objects.filter(
                Q(user_balance_operation__type=self.value())
                & ~Q(type=NotificationType.RETURN_GOODSNSERVICES_PURCHASE)
            )
        return queryset


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Дико дурацкий, польностью переименованный класс для тз, короче дичь"""

    ordering = ["-timestamp"]
    list_per_page = 25

    list_display = [
        "user",
        "timestamp",
        "operation_type",
        "object_type",
        "object_type_name",
    ]
    actions = [notification_report]

    list_filter = (OperationObjectListFilter, OperationTypeListFilter, "timestamp")
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__patronymic_name",
        "user_purchase__goods_n_services_item__name",
        "participation__event__name",
        "initiative__title",
        "vote__name",
    ]

    def operation_type(self, obj: Notification):
        """Пишем возврат, если тип уведомления возврат (в самих операциях баланса такого нет) - по тз"""
        if not obj.user_balance_operation:
            return None
        if obj.type == NotificationType.RETURN_GOODSNSERVICES_PURCHASE:
            return "Возврат"

        return UserBalanceOperationType.RESOLVER[obj.user_balance_operation.type]

    def object_type(self, obj: Notification):
        return NotificationType.RESOLVER[obj.type]

    def object_type_name(self, obj: Notification):
        try:
            if (
                obj.type == NotificationType.EVENT_PARTICIPATION
                or obj.type == NotificationType.DECLINE_EVENT_PARTICIPATION
            ):
                return obj.participation.event.name
            elif (
                obj.type == NotificationType.GOODSNSERVICES_PURCHASE
                or obj.type == NotificationType.RETURN_GOODSNSERVICES_PURCHASE
            ):
                return obj.user_purchase.goods_n_services_item.name
            elif obj.type == NotificationType.VOTING_PARTICIPATION:
                return obj.vote.name
            elif (
                obj.type == NotificationType.ADDING_INITIATIVE
                or obj.type == NotificationType.APPROVE_INITIATIVE
            ):
                return obj.initiative.title
            return None
        except AttributeError:
            return None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    operation_type.short_description = "Тип операции"
    object_type.short_description = "Объект операции"
    object_type_name.short_description = "Наименование объекта операции"
