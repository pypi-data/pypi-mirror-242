from typing import Optional, ItemsView, List, Tuple

from django.apps import apps
from django.conf.urls import url
from django.contrib.admin import SimpleListFilter
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet, Q
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError

from modules.core.models import UserRole, Organization
from modules.core.models.user_action_tracking import ActionTypeEnum, UserActionTracking


class AbstractCustomListFilter(SimpleListFilter):
    template = "core/admin/user_action_tracking/custom_list_filter.html"

    def __init__(self, *args, **kwargs):
        self.values = None
        super(AbstractCustomListFilter, self).__init__(*args, **kwargs)

    @classmethod
    def filter_query_string_error(cls, request: WSGIRequest):
        raise ValidationError(f"Ошибка FilterList: {request.GET}")

    def get_values(self, request):

        result = dict(request.GET).get(self.parameter_name, [""])[0]
        if result != "":
            result = result.split(",")
        else:
            result = []
        return result

    def value(self):
        if hasattr(self, "values") and len(self.values) > 0:
            return self.values
        else:
            return super(AbstractCustomListFilter, self).value()

    @classmethod
    def filter_query_string(cls, request: WSGIRequest) -> str:
        query_string = []
        for key, value in cls.get_lookups():
            if key in request.GET or f"{key}" in request.GET:
                query_string += [f"{key}"]
        query_string = f"{cls.parameter_name}=" + ",".join(query_string)
        return query_string

    def choices(self, changelist):
        """Формирование данных для формы"""
        for lookup, title in self.lookup_choices:
            condition = self.value() == str(lookup)
            if hasattr(self, "values") and self.value():
                condition = str(lookup) in self.value()
            yield {
                "selected": condition,
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
                "field_name": lookup,
                "parameter_name": self.parameter_name,
            }

    def lookups(self, request, model_admin):
        qs: QuerySet = model_admin.get_queryset(request)

        for key, translate_key in self.get_lookups():
            query = self.get_query(key)
            if qs.filter(query).exists():
                yield key, translate_key

    def get_query(self, value: Optional[str]) -> Q:
        raise ValidationError(f"Query error: {value}")

    @classmethod
    def get_lookups(cls) -> ItemsView:
        raise ValidationError(f"Lookups error")

    def queryset(self, request, queryset: QuerySet):
        query = Q()
        self.values = self.get_values(request)
        for item in self.values:
            query |= self.get_query(item)
        result = queryset.filter(query).distinct()
        return result


class SubjectRolesListFilter(AbstractCustomListFilter):
    title = "Роль"
    parameter_name = "subject_roles"

    @classmethod
    def get_lookups(cls) -> ItemsView:
        return UserRole.RESOLVER.items()

    def get_query(self, value: Optional[str]) -> Q:
        if value is None or value == "None":
            return Q(subject_organization__isnull=True)
        value = UserRole.RESOLVER.get(value)
        return Q(subject_roles__icontains=value)

# TODO Объединение справочников 11.11.2023
# class SubjectOrganizationListFilter(AbstractCustomListFilter):
#     title = "Организация"
#     parameter_name = "subject_organization"
#
#     @classmethod
#     def get_lookups(cls) -> ItemsView:
#         queryset: QuerySet = Organization.objects.all().values("name")
#         result = {None: "-"}
#         for index, item in enumerate(queryset, 1):
#             result[item.get("name")] = item.get("name")
#         return result.items()
#
#     def get_query(self, value: Optional[str]) -> Q:
#         if value is None or value == "None":
#             return Q(subject_organization__isnull=True)
#         return Q(subject_organization__icontains=value)


class OperationTypeListFilter(AbstractCustomListFilter):
    title = "Тип операции"
    parameter_name = "operation_type"

    @classmethod
    def get_lookups(cls) -> ItemsView:
        return ActionTypeEnum.RESOLVER.items()

    def get_query(self, value: Optional[str]) -> Q:
        if value is None or value == "None":
            return Q(operation_type__isnull=True) | Q(operation_type="OTHER")
        return Q(operation_type__icontains=value)


class ModuleListFilter(AbstractCustomListFilter):
    title = "Объект операции"
    parameter_name = "module"

    @classmethod
    def _get_project_apps(cls) -> List[Tuple]:
        """Получение списка приложений проекта"""
        project_apps = [
            (item.name.lstrip("modules."), item.verbose_name.split(". ")[-1])
            for item in apps.get_app_configs()
            if hasattr(item, "verbose_name")
        ]
        return project_apps

    @classmethod
    def get_lookups(cls) -> ItemsView:
        result = {None: "-"}
        for item, verbose_name in dict(cls._get_project_apps()).items():
            result[verbose_name] = verbose_name
        return result.items()

    def get_query(self, value: Optional[str]) -> Q:
        if value is None or value == "None":
            return Q(module__isnull=True)
        return Q(module__icontains=value)


class ObjectNameListFilter(AbstractCustomListFilter):
    title = "Наименование объекта операции"
    parameter_name = "object_name"

    @classmethod
    def _get_project_apps(cls) -> List[Tuple]:
        """Получение списка приложений проекта"""
        project_apps = [
            (item.name.lstrip("modules."), item.verbose_name.split(". ")[-1])
            for item in apps.get_app_configs()
            if hasattr(item, "verbose_name") and "modules" in item.name
        ]
        return project_apps

    @classmethod
    def _get_project_models(cls) -> List[Tuple]:
        """Получение списка моделей проекта"""
        project_apps = cls._get_project_apps()
        project_models = []
        for app in project_apps:
            app_models = {}
            if apps.all_models.get(app[0], None):
                app_models = apps.get_app_config(app[0]).get_models()
            for model in app_models:
                value = (model.__name__, model._meta.verbose_name)
                project_models.append(value)
        return project_models

    @classmethod
    def get_lookups(cls) -> ItemsView:
        result = {None: "-"}
        for item, verbose_name in dict(cls._get_project_models()).items():
            result[verbose_name] = verbose_name
        return result.items()

    def get_query(self, value: Optional[str]) -> Q:
        if value is None or value == "None":
            return Q(object_name__isnull=True)
        return Q(object_name__icontains=value)


class LocalityListFilter(AbstractCustomListFilter):
    title = "Населённый пункт (МО)"
    parameter_name = "locality"

    @classmethod
    def get_lookups(cls) -> ItemsView:
        queryset: QuerySet = UserActionTracking.objects.all().values("locality")
        result = {}
        for index, item in enumerate(queryset, 1):
            result[item.get("locality")] = item.get("locality")
        result[None] = "-"
        return result.items()

    def get_query(self, value: Optional[str]) -> Q:
        if value is None or value == "None":
            return Q(locality__isnull=True)
        return Q(locality__icontains=value)


class CustomListFiltersMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_filter = [
            # SubjectOrganizationListFilter,
            SubjectRolesListFilter,
            OperationTypeListFilter,
            ModuleListFilter,
            ObjectNameListFilter,
            LocalityListFilter,
        ] + list(self.list_filter[:])

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                "custom_filter/$",
                self.custom_filter,
                name="custom_filter",
            ),
        ]
        return custom_urls + urls

    def custom_filter(
        self,
        request: WSGIRequest,
    ):
        filters = {}
        for item in self.list_filter:
            if hasattr(item, "parameter_name") and issubclass(
                item, AbstractCustomListFilter
            ):
                filters[item.parameter_name] = item.filter_query_string
        get_request_data = request.GET
        parameter_name = {
            "parameter_name": value for value in get_request_data.values()
        }.get("parameter_name")
        query_string = ""
        if len(get_request_data) > 0:
            query_string = filters.get(
                parameter_name, AbstractCustomListFilter.filter_query_string_error
            )(request)
        return redirect(f"../?{query_string}")
