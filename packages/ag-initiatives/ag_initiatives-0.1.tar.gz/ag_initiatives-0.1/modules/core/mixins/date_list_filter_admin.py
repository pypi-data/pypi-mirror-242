import datetime

from django.conf.urls import url
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import FieldError
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet, Q
from django.shortcuts import redirect
from django.utils import timezone


class DateListFilter(SimpleListFilter):
    """
    Фильтрация объектов модели по дате
    Класс основан на SimpleListFilter
    Формирование входных данных происходит
    на основе GET-параметров запроса и набора
    данных из класса ModelAdmin
    Для применения в панелях администратора
    необходимо изменить наименование полей в
    методе get_query() на соответствующие поля модели
    Для работы фильтра необходим шаблон.
    """

    # путь до шаблона приложения
    template = "core/admin/user_action_tracking/custom_date_filter.html"
    # название параметра (поля модели) для фильтрации
    parameter_name = "timestamp"
    # заголовок фильтра
    title = "Дата операции"
    # формат даты фильтра
    date_format = "%Y-%m-%d"

    def __init__(self, *args, **kwargs):
        self.values = None
        self.min_date = timezone.datetime.now().astimezone().strftime(self.date_format)
        self.max_date = timezone.datetime.now().astimezone().strftime(self.date_format)
        self.re_parameter = self.set_date_regular_expression()
        super(DateListFilter, self).__init__(*args, **kwargs)

    @staticmethod
    def set_date_regular_expression() -> str:
        """Проверка строковой даты на соответствие маскам [YYYY-MM-DD]|[YYYY-M-D]"""
        re_parameter_year = "^(19|20)\d\d"
        re_parameter_month = "(((0[1-9]{1})|([1-9]{1}))|(1[1-2]{1}))"
        re_parameter_day = "(([1-9]{1}|0[1-9]{1})|(1\d)|(2\d)|(3[0-1]{1}))$"
        re_parameter = f"{re_parameter_year}-{re_parameter_month}-{re_parameter_day}"
        return re_parameter

    @staticmethod
    def date_chek(date):
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return None

    def lookups(self, request: WSGIRequest, model_admin):
        """Перечень параметров фильтра"""
        return ("start_date", "От"), ("end_date", "До")

    def get_values(self, request: WSGIRequest):
        """Выборка параметров запроса"""
        result = dict(request.GET).get(self.parameter_name, [])
        return result

    def queryset(self, request: WSGIRequest, queryset: QuerySet):
        """Формирование наборы данных"""
        self.min_date = self.get_min_date_value(queryset)
        self.max_date = self.get_max_date_value(queryset)
        self.values = self.get_values(request)
        query = self.get_query(self.values)
        result = queryset.none()
        try:
            result = queryset.filter(query).distinct()
        except FieldError as e:
            if any(["DateField" in item for item in e.args]):
                query = self.get_query(self.values, advanced="")
                result = queryset.filter(query).distinct()
        return result

    def get_query(self, values, advanced="__date") -> Q:
        """
        Формирование фильтра для набора данных
        Для масштабирования необходимо изменить название полей в Q()
        """
        query = Q()
        if values is None or values == "None" or values == [] or values == [""]:
            return query
        if self.date_chek(values[0]) is not None:
            start_date = (
                timezone.datetime.strptime(values[0], self.date_format)
                .astimezone()
                .date()
            )
            string = f"Q({self.parameter_name}{advanced}__gte=start_date)"
            query &= eval(string)
        if self.date_chek(values[-1]) is not None:
            end_date = (
                timezone.datetime.strptime(values[-1], self.date_format)
                .astimezone()
                .date()
            )
            string = f"Q({self.parameter_name}{advanced}__lte=end_date)"
            query &= eval(string)
        return query

    @classmethod
    def get_instance_field_data(cls, instance, field):
        if hasattr(instance, field):
            return eval(f"instance.{field}")
        return None

    @classmethod
    def get_min_date_value(cls, queryset: QuerySet):
        """Формирование начальной даты"""
        min_date = timezone.datetime.now().astimezone().strftime(cls.date_format)
        if queryset.exists():
            instance = queryset.order_by(cls.parameter_name).first()
            field_value = cls.get_instance_field_data(instance, cls.parameter_name)
            if isinstance(field_value, timezone.datetime):
                min_date = field_value.astimezone().strftime(cls.date_format)
        return min_date

    @classmethod
    def get_max_date_value(cls, queryset: QuerySet):
        """Формирование конечной даты"""
        max_date = timezone.datetime.now().astimezone().strftime(cls.date_format)
        if queryset.exists():
            instance = queryset.order_by(cls.parameter_name).last()
            field_value = cls.get_instance_field_data(instance, cls.parameter_name)
            if isinstance(field_value, timezone.datetime):
                max_date = field_value.astimezone().strftime(cls.date_format)
        return max_date

    def get_field_data(self) -> dict:
        """Формирование значений для полей формы"""
        field_data = {
            "start_date": self.min_date,
            "end_date": self.max_date,
        }
        if self.values and len(self.values) == 2:
            if self.date_chek(self.values[0]):
                field_data["start_date"] = self.values[0]
            if self.date_chek(self.values[-1]):
                field_data["end_date"] = self.values[-1]
        return field_data

    def find_error_in_dates(self, field_data: dict) -> bool:
        """Проверка значений начальной и конечной даты"""
        start_date = (
            timezone.datetime.strptime(field_data["start_date"], self.date_format)
            .astimezone()
            .date()
        )
        end_date = (
            timezone.datetime.strptime(field_data["end_date"], self.date_format)
            .astimezone()
            .date()
        )
        return start_date > end_date

    def choices(self, changelist):
        """Формирование данных для формы"""
        field_data = self.get_field_data()
        date_error = self.find_error_in_dates(field_data)
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
                "field_name": lookup,
                "parameter_name": self.parameter_name,
                "value": field_data.get(lookup, "2000-1-1"),
                "min": self.min_date,
                "max": self.max_date,
                "date_error": date_error,
            }


class DateListFilterMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_filter = [DateListFilter] + list(self.list_filter[:])

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                "custom_date_filter/$",
                self.custom_date_filter,
                name="custom_date_filter",
            ),
        ]
        return custom_urls + urls

    def custom_date_filter(self, request: WSGIRequest):
        """Метод для обработки GET-запроса с данными формы"""
        # переменные start_date и end_date заложены
        # в настройках фильтра, их можно переопределить
        # в методе lookups()
        start_date = request.GET.get("start_date", "")
        end_date = request.GET.get("end_date", "")
        # для использования фильтра необходимо использовать
        # переменную parameter_name соответствующего класса
        # raise ValidationError(request.GET)
        parameter_name = DateListFilter.parameter_name
        query_string = f"{parameter_name}={start_date}&{parameter_name}={end_date}"
        if request.GET.get("clear", False):
            query_string = ""
        return redirect(f"../?{query_string}")
