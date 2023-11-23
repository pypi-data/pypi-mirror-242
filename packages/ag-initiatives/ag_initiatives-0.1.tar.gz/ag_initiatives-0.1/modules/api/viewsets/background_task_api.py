from typing import Union

from django.http import HttpResponse
from django.utils import timezone
from gunicorn.config import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from modules.api.filters.report_type_filter import ReportTypeFilter
from modules.core.exceptions import ReportTypeError
from modules.core.exceptions import EmptyVoteError
from modules.core.services import BackgroundTaskProcessingService


class BackgroundTaskApi(viewsets.ViewSet):
    """
    === API BackgroundTaskApi

    Доступ:

    * IsAuthenticated

    Служба - BackgroundTaskProcessingService

    Фильтр типов - ReportTypeFilter

    Эндпоинты:

    * ask-report - methods: GET; detail: False;
    * report-types - methods: GET; detail: False;
    * check-report-status - methods: GET; detail: True; key: celery_key (ask-report);
    * get-report - methods: GET; detail: True; key: cache_key (check-report-status:task_result);
    * get-report-directly - methods: GET; detail: True; key: Vote.id;
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    service = BackgroundTaskProcessingService
    type_filter = ReportTypeFilter

    @action(methods=["get"], detail=False, url_path="ask-report", url_name="ask-report")
    def ask_report(self, request) -> Response:
        """Запрос на формирование отчёта по типу"""
        report_types = dict(request.GET.copy()).get("type")
        votes = dict(request.GET.copy()).get("vote")
        user = request.user
        if not report_types:
            raise ReportTypeError(report_types)
        if not votes:
            raise EmptyVoteError()
        cleared_report_types = self.service.clear_report_types(report_types)
        cleared_votes = self.service.clear_votes(votes)
        celery_task = self.service.run_report_generator.delay(
            f"{user}", cleared_report_types, cleared_votes
        )
        return Response({"celery_key": celery_task.id}, status=status.HTTP_202_ACCEPTED)

    @action(
        methods=["get"], detail=False, url_path="report-types", url_name="report-types"
    )
    def report_types(self, request) -> Response:
        """Перечень типов отчётов"""
        data = self.type_filter(**request.GET.copy()).data
        return Response(data, status=status.HTTP_202_ACCEPTED)

    @action(
        methods=["get"],
        detail=True,
        url_path="check-report-status",
        url_name="check-report-status",
    )
    def get_task_status_in_celery(self, request, pk) -> Response:
        """Проверка статуса формирования отчёта в Celery"""
        data = self.service.get_celery_task_status_with_async_result(pk)
        if data["task_status"] == "PENDING":
            response_status = status.HTTP_204_NO_CONTENT
        elif data["task_status"] == "SUCCESS":
            response_status = status.HTTP_200_OK
        else:
            response_status = status.HTTP_404_NOT_FOUND
        return Response(data, status=response_status)

    @action(methods=["get"], detail=True, url_path="get-report", url_name="get-report")
    def get_report_from_cache(self, request, pk) -> Union[Response, HttpResponse]:
        """Получение данных отчёта из кэша"""
        cache_data = self.service.get_generated_report_file_from_cache(pk)
        if cache_data:
            return self.service.make_response_from_cache_data(cache_data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=["get"],
        detail=True,
        url_path="get-report-directly",
        url_name="get-report-directly",
        permission_classes=[IsAuthenticated],
    )
    def get_report_directly(self, request, pk) -> Union[Response, HttpResponse]:
        """Получение отчёта напрямую"""
        report_types = dict(request.GET.copy()).get("type")
        user = request.user if request.user.is_authenticated else ""
        if not report_types or len(report_types) == 0:
            raise ReportTypeError(report_types)
        cleared_report_type = self.service.clear_report_types(report_types)[0]
        result = self.service.get_single_report(f"{user}", cleared_report_type, pk)
        if not result.get("error"):
            return self.service.make_response_from_cache_data(result)
        return Response(result, status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=["get"],
        detail=False,
        url_path="get-user_list",
        url_name="get-user_list",
        permission_classes=[AllowAny],
    )
    def get_user_list(self, request):
        """Получение отчёта напрямую"""
        user = request.user if request.user.is_authenticated else User.objects.none()
        result = self.service.get_user_list_report(user.id)
        if not result.get("error"):
            return self.service.make_response_from_cache_data(result)
        return Response(result, status=status.HTTP_404_NOT_FOUND)
