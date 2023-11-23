"""
=== Служба обработки задач

Служба отвечает за создание задачи для работников celery.

Вход:

* Данные для задачи

Выход:

* Идентификатор задачи в системе

Зависимости:

* Модель BackgroundTask

"""
import json
import time
import uuid
from io import BytesIO
from typing import Dict, Optional, Any, List, Union

import openpyxl
import redis
from celery import shared_task
from celery.result import AsyncResult
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from config.settings import CACHE_TIMEOUT

from modules.core.enum import ReportTypeEnum
from modules.core.exceptions import ReportTypeError
from modules.core.models import User
from modules.core.services.excel_from_dict.books import Book
from modules.core.services.excel_from_dict.handlers import (
    ExcelHandler,
    RegionalVoteReport,
    MunicipalVoteReport,
    LocalVoteReport,
)
from modules.core.services.excel_from_dict.handlers.user_list_report import (
    UserListReport,
)


class BackgroundTaskProcessingService(object):
    """
    === Служба BackgroundTaskProcessingService (Обработка фоновых задач)

    Методы:

    * get_celery_task_status_with_async_result - получение статуса задачи Celery;
    +
    ----
    (celery_key: uuid.uuid4) -> Dict
    ----
    * get_generated_report_file_from_cache - получить сгенерированный файл отчёта из кэша;
    +
    ----
    (cache_key: uuid.uuid4) -> Dict
    ----
    * clear_report_types - форматирование типов отчёта из GET-запроса;
    +
    ----
    (report_types: Union[str, List]) -> List
    ----
    * clear_votes - форматирование идентификаторов голосования из GET-запроса;
    +
    ----
    (votes: Union[str, List]) -> List[str]
    ----
    * get_single_report - получение одного отчёта по голосованию и типу;
    +
    ----
    (user: str, report_type: str, vote_id: Union[str, int]
    ) -> Dict
    ----
    * _get_report_types_objects - получение списка типов отчёта из списка строк;
    +
    ----
    (report_types: List[str]) -> List[ReportTypeEnum]
    ----
    * run_report_generator - генератор отчётов;
    +
    ----
    (report_types: Union[str, List]) -> Dict
    ----
    * make_response_from_cache_data - получение отчёта из кэша;
    +
    ----
    (cache_data: Dict) -> HttpResponse
    ----
    """

    @classmethod
    def get_celery_task_status_with_async_result(cls, celery_key: uuid.uuid4) -> Dict:
        """Получение статуса задачи Celery"""
        task_result = AsyncResult(celery_key)
        return {
            "task_key": celery_key,
            "task_status": task_result.status,
            "task_result": task_result.result,
        }

    @classmethod
    def get_generated_report_file_from_cache(cls, cache_key: uuid.uuid4) -> Dict:
        """Получить сгенерированный файл отчёта из кэша"""
        return cache.get(f"vote_report_{cache_key}")

    @classmethod
    def clear_report_types(cls, report_types: Union[str, List]) -> List[str]:
        """Форматирование типов отчёта из GET-запроса"""

        result = []
        if isinstance(report_types, str):
            report_types = report_types.split(",")
        for item in report_types:
            if "," in item:
                result += item.split(",")
            else:
                result += [item]
        return result

    @classmethod
    def clear_votes(cls, votes: Union[str, List]) -> List[str]:
        """Форматирование идентификаторов голосования и GET-запроса"""
        result = []
        if isinstance(votes, str):
            votes = votes.split(",")
        for item in votes:
            if "," in item:
                result += item.split(",")
            else:
                result += [item]
        return result

    @classmethod
    def get_single_report(
        cls, user: str, report_type: str, vote_id: Union[str, int]
    ) -> Dict:
        """Получение одного отчёта по голосованию и типу"""
        result = {}
        report_types_object = cls._get_report_types_objects([report_type])[0]
        report = dict()
        if report_types_object.name in ReportTypeEnum.regional_reports():
            report = RegionalVoteReport(report_types_object, user, vote_id)
        elif report_types_object.name in ReportTypeEnum.municipal_reports():
            report = MunicipalVoteReport(report_types_object, user, vote_id)
        elif report_types_object.name in ReportTypeEnum.local_reports():
            report = LocalVoteReport(report_types_object, user, vote_id)
        binary: BytesIO = report.get()
        result["binary_file"] = binary
        result["vote_id"] = vote_id
        result["report_type"] = report_types_object.name.capitalize()
        return result

    @classmethod
    def _get_report_types_objects(cls, report_types: List[str]) -> List[ReportTypeEnum]:
        """Получение списка типов отчёта из списка строк"""
        result = []
        for index, report_type in enumerate(report_types):
            instance = ReportTypeEnum.get_instance(report_type)
            result.append(instance)
            if instance is None:
                raise ReportTypeError(report_type)
        return result

    @staticmethod
    @shared_task
    def run_report_generator(user: str, report_types: List[str], votes: List) -> List:
        """Генератор отчётов"""
        result = []
        count = 0
        for report_type in report_types:
            for pk in votes:
                try:
                    report_data = BackgroundTaskProcessingService.get_single_report(
                        user, report_type, pk
                    )
                    cache_key = f"vote_report_{uuid.uuid4()}"
                    cache.set(
                        cache_key,
                        report_data,
                        timeout=CACHE_TIMEOUT,
                    )
                    result.append(
                        {
                            count: {
                                "cache_key": cache_key.lstrip("vote_report_"),
                                "vote_id": pk,
                                "report": report_type,
                            }
                        }
                    )
                except Exception as e:
                    result.append(
                        {"error": f"{e}", "report_type": report_type, "vote": pk}
                    )
                count += 1
        return result

    @classmethod
    def make_response_from_cache_data(cls, cache_data: Dict) -> HttpResponse:
        """Получение отчёта из кэша"""
        binary_file = cache_data.get("binary_file")
        vote = cache_data.get("vote_id")
        report_type = str(cache_data.get("report_type")).capitalize()
        today = timezone.now().astimezone().strftime("%Y-%m-%d %H%M%S")
        # content_type = "application/excel"
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response_status = 200
        response = HttpResponse(content_type=content_type, status=response_status)
        filename = f"{today}-Vote_{vote}-{report_type}"
        response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'

        binary_file.seek(0)
        response.write(binary_file.read())
        return response

    @classmethod
    def get_user_list_report(cls, user_id):
        """Получение одного отчёта по голосованию и типу"""
        result = {}
        report = dict()
        result["report_type"] = ReportTypeEnum.USER_LIST_REPORT
        report = UserListReport(result["report_type"], user_id)

        binary: BytesIO = report.get()
        result["binary_file"] = binary
        return result
