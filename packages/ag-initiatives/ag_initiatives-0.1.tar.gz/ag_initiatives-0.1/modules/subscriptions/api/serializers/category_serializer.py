from collections import OrderedDict
from typing import List

from django.apps import apps

from modules.subscriptions.enums import ActiveCitizenModuleEnum


class CategorySerializer(object):
    """Сериализатор категорий отслеживаемых моделей"""

    @classmethod
    def _format_category_data(cls, instance) -> dict:
        """Формирование данных по объекту Категории"""
        model = instance.__class__
        app_label = (
            model._meta.app_label if model._meta.app_label != "plans" else "core"
        )
        category_id = instance.id
        category_name = f"{instance}"
        category_parent: dict = cls._get_parents(instance)
        category_text_link = f"{app_label}:{model.__name__}:{instance.id}"
        data = OrderedDict(
            {
                "id": category_id,
                "name": category_name,
                "parent": category_parent,
                "text_link": category_text_link,
            }
        )
        return data

    @classmethod
    def _get_categories_list(cls, model) -> List:
        """Формирование перечня объектов Категории"""
        categories_list = []
        for instance in model.objects.all():
            category_data = cls._format_category_data(instance)
            categories_list.append(category_data)
        return categories_list

    @classmethod
    def _get_model_data(cls, app_label: str) -> List:
        """Формирование данных по моделям приложения"""
        model_data = []
        app_models = [
            model
            for model in apps.get_app_config(app_label).get_models()
            if "category" in f"{model.__name__}".lower()
            and "department" not in f"{model.__name__}".lower()
        ]
        for model in app_models:
            category_data = OrderedDict()
            category_data["module"] = f"{app_label}"
            category_data["model_name"] = f"{model.__name__}"
            category_data["verbose_name"] = f"{model._meta.verbose_name}"
            category_data["categories_list"] = cls._get_categories_list(model)
            model_data.append(category_data)
        return model_data

    @classmethod
    def _get_parents(cls, instance) -> dict:
        """Рекурсивное получение данных по родительским категориям"""
        result = {}
        if hasattr(instance, "parent") and instance.parent:
            return cls._format_category_data(instance.parent)
        return result

    @classmethod
    def data(cls) -> List:
        """Формирование выходных данных API"""
        data = []
        for app in ActiveCitizenModuleEnum.RESOLVER.keys():
            app_label = app
            if app == "ap_works":
                app_label = "map_works"
            data += cls._get_model_data(app_label)
        return data
