from collections import OrderedDict
from typing import List, Tuple

from django.apps import apps


def get_project_apps() -> List[Tuple]:
    """Получение списка приложений проекта"""
    project_apps = [
        (item.name.lstrip("modules."), item.verbose_name.split(". ")[-1])
        for item in apps.get_app_configs()
        if hasattr(item, "verbose_name")
    ]
    return project_apps


@classmethod
def get(cls, value):
    """Выборка отображаемого значения по ключу"""
    return cls.RESOLVER.get(value, None)


@classmethod
def get_app_by_model(cls, instance):
    """Приложение, к которому относится объект модели"""
    result = instance._meta.app_label
    if result == "map_works":
        result = "".join([item for item in result[1:]])
    return result


@classmethod
def to_json(cls) -> List:
    result = [OrderedDict({"name": key, "value": value}) for key, value in cls.CHOICES]
    return result


required_modules = ["voting", "core", "plans", "initiatives", "ap_works"]

modules = [
    (item[0], item[-1].split(". ")[-1])
    for item in get_project_apps()
    if item[0] in required_modules
]
resolver = OrderedDict({item[0]: item[1] for item in modules})
fields = OrderedDict({item[0]: item[0] for item in modules})
fields.update({"RESOLVER": resolver})
fields.update({"CHOICES": resolver.items()})
fields.update({"get": get})
fields.update({"get_app_by_model": get_app_by_model})
fields.update({"__doc__": """Список модулей проекта"""})
fields.update({"__json__": to_json})
ActiveCitizenModuleEnum = type("ActiveCitizenModuleEnum", (), fields)
