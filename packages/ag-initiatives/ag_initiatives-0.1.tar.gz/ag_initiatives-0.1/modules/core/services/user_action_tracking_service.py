from collections import OrderedDict
from datetime import datetime
from functools import wraps
from typing import List, Optional, Union, Tuple, Any

from django.apps import apps
from django.contrib.admin import ModelAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.forms import forms
from rest_framework.request import Request

from modules.core.models import User, UserRole
from modules.core.models.user_action_tracking import ActionTypeEnum, UserActionTracking


class UserActionTrackingService(object):
    """Сервис учёта действий пользователя"""

    def __init__(self, action: List[str]):
        self.model = None
        self.actions = self._get_action(action)

    def __call__(self, func):

        entry_data = OrderedDict(
            {
                "timestamp": self._get_timestamp(),
                "subject": None,
                "subject_roles": None,
                "subject_organization": None,
                "module": None,
                "object_name": None,
                "operation_type": None,
                "locality": None,
                "value_before": None,
                "value_after": None,
            }
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Обёртка для выполнения декорируемой функции и подготовки данных для журнала"""
            nonlocal entry_data
            request, obj, form, change = self._get_function_arguments(*args, **kwargs)
            self.model = obj.__class__

            user = self._get_user(*args, **kwargs)
            entry_data.update(self._get_base_data(user))
            entry_data["module"] = {
                "module": module[-1]
                for module in self._get_project_apps()
                if self.model._meta.app_label in module[0]
            }.get("module", "")
            entry_data["object_name"] = self.model._meta.verbose_name

            varriants = {
                "CREATE": self._create_action,
                "DELETE": self._delete_action,
                "UPDATE": self._update_action,
            }

            if change:
                action = ActionTypeEnum.UPDATE
            else:
                action = self.actions[0]
            if action == "CREATE":
                result = func(*args, **kwargs)
            object_data = self._get_object_data(obj)

            if "locality" in object_data:
                entry_data["locality"] = object_data["locality"]
                object_data.pop("locality")
            if action in varriants:
                entry_data.update(varriants[action](object_data, *args, **kwargs))
                self._insert_entry_to_journal(entry_data)
            if action != "CREATE":
                result = func(*args, **kwargs)
            return result

        return wrapper

    @classmethod
    def _get_function_arguments(
        cls,
        sender: ModelAdmin,
        request: WSGIRequest,
        obj,
        form: Optional[forms.Form] = None,
        change: Optional[bool] = False,
        *args,
        **kwargs,
    ):
        """Получение данных из функций сохранения и удаления объекта"""
        return request, obj, form, change

    @classmethod
    def _get_project_apps(cls) -> List[Tuple]:
        """Получение списка приложений проекта"""
        project_apps = [
            (item.name.lstrip(".modules"), item.verbose_name.split(". ")[-1])
            for item in apps.get_app_configs()
            if hasattr(item, "verbose_name")
        ]
        return project_apps

    def _get_action(self, action_list: List[str]) -> List[ActionTypeEnum]:
        """Получение перечня действий"""
        result = []
        for item in ActionTypeEnum.RESOLVER.keys():
            for action_name in action_list:
                if f"{action_name}".lower() == f"{item}".lower():
                    result.append(item)
        if len(result) == 0:
            return [ActionTypeEnum.OTHER]
        return result

    @staticmethod
    def _get_user_data(user: Optional[User]) -> Optional[str]:
        """Получение данных пользователя (ФИО)"""
        return f"{user}" if user else None

    @staticmethod
    def _get_timestamp() -> datetime:
        """Получение временной метки"""
        try:
            from django.utils import timezone

            timestamp = timezone.now().astimezone()
        except ModuleNotFoundError:
            from datetime import datetime

            timestamp = datetime.now()
        return timestamp

    @staticmethod
    def _get_roles(user: Optional[Union[User, str]] = None) -> str:
        """Получение ролей пользователя"""
        if not user or isinstance(user, str) and user.lower() == "system":
            return "SYSTEM"
        elif user.is_anonymous:
            return "ANONYMOUS"
        else:
            return ";".join([
                UserRole.RESOLVER.get(role, "SYSTEM")
                for role in user.roles
            ])

    @staticmethod
    def _get_organization(user: Optional[User] = None) -> Optional[str]:
        """Получение организации пользователя"""
        if not user:
            return None
        elif user.is_anonymous:
            return None
        elif not user.department:
            return None
        return user.department.name

    @staticmethod
    def _get_user(*args, **kwargs) -> Optional[User]:
        """Выборка пользователя из запроса"""
        user = None
        if not kwargs.get("request"):
            for item in args:
                if type(item) in (WSGIRequest, Request) and hasattr(item, "user"):
                    user = item.user
        else:
            user = kwargs.get("request").user
        return user

    @classmethod
    def _get_base_data(cls, user: Optional[User]) -> dict:
        """Формирование базовых данных для журнала"""
        base_data = OrderedDict()
        base_data["subject"] = cls._get_user_data(user)
        base_data["subject_organization"] = cls._get_organization(user)
        base_data["subject_roles"] = cls._get_roles(user)
        return base_data

    @classmethod
    def _insert_entry_to_journal(cls, data: dict) -> None:
        """Добавление записи в журнал"""
        if data["value_before"] != data["value_after"]:
            UserActionTracking.objects.create(**data)
        return

    def _get_old_object_data(self, object_data):
        """Получение данных объекта перед изменением"""
        obj = self.model.objects.filter(pk=object_data.get("id", 0)).first()
        data = self._get_object_data(obj)
        return data

    def _create_action(self, object_data, *args, **kwargs) -> dict:
        """Формирование данных для журнала по действию создания объекта модели"""
        entry_data = OrderedDict()
        entry_data["operation_type"] = ActionTypeEnum.CREATE
        entry_data["value_before"] = None
        entry_data["value_after"] = ";".join(
            [
                self._get_string_view_for_value(key, value)
                for key, value in object_data.items()
            ]
        )
        return entry_data

    def _update_action(self, object_data, *args, **kwargs) -> dict:
        """Формирование данных для журнала по действию обновления объекта модели"""
        entry_data = OrderedDict()
        old_data = self._get_old_object_data(object_data)
        unmodified_fields = []
        for new_field, new_value in object_data.items():
            for old_field, old_value in old_data.items():
                condition = [
                    new_field == old_field,
                    new_value == old_value,
                    new_field != "id",
                ]
                if all(condition):
                    unmodified_fields.append(new_field)
        for field_name in unmodified_fields:
            object_data.pop(field_name)
            old_data.pop(field_name)
        entry_data["operation_type"] = ActionTypeEnum.UPDATE

        entry_data["value_before"] = ";".join(
            [
                self._get_string_view_for_value(key, value)
                for key, value in old_data.items()
                if key in object_data.keys()
            ]
        )
        entry_data["value_after"] = ";".join(
            [
                self._get_string_view_for_value(key, value)
                for key, value in object_data.items()
                if key in old_data.keys()
            ]
        )

        return entry_data

    def _delete_action(self, object_data, *args, **kwargs) -> dict:
        """Формирование данных для журнала по действию удаления объекта модели"""
        entry_data = OrderedDict()
        entry_data["operation_type"] = ActionTypeEnum.DELETE
        entry_data["value_before"] = ";".join(
            [
                self._get_string_view_for_value(key, value)
                for key, value in object_data.items()
            ]
        )
        entry_data["value_after"] = None
        return entry_data

    def _get_string_view_for_value(self, *data: Any) -> str:
        """Ф"""
        for field in self.model._meta.fields:
            if field.name == data[0]:
                key = (
                    [field.verbose_name, "Идентификатор"]
                    [field.verbose_name == "ID"]
                )
                return f"{key}: {data[-1]}"
        return f"{data[0]}: {data[-1]}"

    def _get_object_data(self, obj) -> dict:
        """Получение данных объекта"""
        object_data = {}
        model_fields = self._get_models_fields()
        for item in model_fields.keys():
            object_data[item] = eval(f"obj.{item}")
            if isinstance(object_data[item], datetime):
                object_data[item] = object_data[item].astimezone().isoformat()
        if hasattr(obj, "locality"):
            if obj.locality.__class__.__name__ == 'ManyRelatedManager':
                object_data["locality"] = ", ".join(
                    [locality.name for locality in obj.locality.all()])
            else:
                object_data["locality"] = f"{obj.locality}"
        return object_data

    def _get_models_fields(self) -> dict:
        return {item.name: None for item in self.model._meta.fields}
