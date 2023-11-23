import collections
from typing import Optional

from django.utils import timezone
from rest_framework import serializers

from config import settings
from modules.api.serializers import LocalitySerializer
from modules.api.serializers.locality import LocalityWithParentSerializer
from modules.ecology.api.serializers.excel import ExcelSerializer

from modules.map_works.api.serializers import (
    WorkCategorySerializer,
    WorkReasonSerializer,
    InstitutionTypeSerializer,
    WorkTypeSerializer,
    ContractorSerializer,
    LocationSerializer,
)
from modules.map_works.models import Works


class WorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = "__all__"


class WorksListSerializer(serializers.ModelSerializer):
    locality = LocalityWithParentSerializer()
    category = WorkCategorySerializer()
    locations = LocationSerializer(many=True)

    class Meta:
        model = Works
        fields = [
            "id",
            "begin_datetime",
            "end_datetime",
            "locality",
            "locations",
            "category",
            "state",
            "state_label",
        ]


class WorksList2Serializer(serializers.ModelSerializer):
    # locality = LocalitySerializer()
    # category = WorkCategorySerializer()
    # reason = WorkReasonSerializer()
    # institution_type = InstitutionTypeSerializer()
    # work_type = WorkTypeSerializer()
    # contractor = ContractorSerializer()
    # locations = LocationSerializer(many=True)

    class Meta:
        model = Works
        fields = [
            "id",
            "locality",
            "category",
            "reason",
            "begin_datetime",
            "end_datetime",
            "private_territory",
            "institution_type",
            "locations",
            "work_type",
            "description",
            "objects_description",
            "contractor",
            "state",
            "state_label",
        ]


class WorksDetailsSerializer(serializers.ModelSerializer):
    locality = LocalitySerializer()
    category = WorkCategorySerializer()
    reason = WorkReasonSerializer()
    institution_type = InstitutionTypeSerializer()
    work_type = WorkTypeSerializer()
    contractor = ContractorSerializer()
    locations = LocationSerializer(many=True)

    class Meta:
        model = Works
        fields = [
            "id",
            "locality",
            "category",
            "reason",
            "begin_datetime",
            "end_datetime",
            "private_territory",
            "institution_type",
            "locations",
            "work_type",
            "description",
            "objects_description",
            "contractor",
            "state",
            "state_label",
        ]


class WorksCreateSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, required=True)

    class Meta:
        model = Works
        fields = [
            "category",
            "reason",
            "begin_datetime",
            "end_datetime",
            "private_territory",
            "institution_type",
            "locality",
            "work_type",
            "description",
            "objects_description",
            "contractor",
            "locations",
        ]


class WorksExcelSerializer(ExcelSerializer):

    locality = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    reason = serializers.SerializerMethodField()
    begin_datetime = serializers.SerializerMethodField()
    end_datetime = serializers.SerializerMethodField()
    private_territory = serializers.SerializerMethodField()
    institution_type = serializers.SerializerMethodField()
    work_type = serializers.SerializerMethodField()
    contractor = serializers.SerializerMethodField()
    is_published = serializers.SerializerMethodField()

    SHEET_NAME = "Ремонтные работы"
    FILE_NAME = "works operations"

    COLUMN_SIZES = 30

    HEADER_MAPPING = {
        "locality": "Муниципальное образование",
        "category": "Категория",
        "reason": "Причина",
        "begin_datetime": "Дата-время начала работ",
        "end_datetime": "Дата-время окончания работ",
        "private_territory": "Частный сектор",
        "institution_type": "Тип учреждения",
        "work_type": "Тип работ",
        "contractor": "Подрядчик",
        "is_published": "Опубликовано",
    }

    class Meta:
        model = Works
        fields = [
            "locality",
            "category",
            "reason",
            "begin_datetime",
            "end_datetime",
            "private_territory",
            "institution_type",
            "work_type",
            "contractor",
            "is_published",
        ]

    def get_locality(self, instance: Works) -> str:
        return instance.locality.name

    def get_category(self, instance: Works) -> str:
        return instance.category.name

    def get_reason(self, instance: Works) -> str:
        return instance.reason.name if instance.reason else None

    def get_begin_datetime(self, instance: Works) -> Optional[str]:
        try:
            time_zone = timezone.get_current_timezone() if settings.USE_TZ else None

            if not time_zone:
                date = instance.begin_datetime.date()
                time = instance.begin_datetime.time().strftime('%H%M')
                return f'{date} {time}'

            date = instance.begin_datetime.astimezone(time_zone).date()
            time = instance.begin_datetime.astimezone(time_zone).time().strftime('%H:%M')
            return f'{date} {time}'
        except AttributeError:
            return None

    def get_end_datetime(self, instance: Works) -> Optional[str]:
        try:
            time_zone = timezone.get_current_timezone() if settings.USE_TZ else None

            if not time_zone:
                date = instance.end_datetime.date()
                time = instance.end_datetime.time().strftime('%H%M')
                return f'{date} {time}'

            date = instance.end_datetime.astimezone(time_zone).date()
            time = instance.end_datetime.astimezone(time_zone).time().strftime('%H:%M')
            return f'{date} {time}'
        except AttributeError:
            return None

    def get_private_territory(self, instance: Works) -> str:
        if instance.private_territory:
            return "Да"
        return "Нет"

    def get_institution_type(self, instance: Works) -> str:
        return instance.institution_type.name if instance.institution_type else None

    def get_work_type(self, instance: Works) -> str:
        return instance.work_type.name if instance.work_type else None

    def get_contractor(self, instance: Works) -> str:
        return instance.contractor.name

    def get_is_published(self, instance: Works) -> str:
        if instance.is_published:
            return "Да"
        return "Нет"
