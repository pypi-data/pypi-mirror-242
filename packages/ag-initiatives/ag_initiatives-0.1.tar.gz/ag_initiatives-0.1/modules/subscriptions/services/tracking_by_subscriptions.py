import importlib
import importlib.util
import sys
from functools import wraps
from typing import List, Union, Optional, Any

from django.core.mail import EmailMessage
from django.db.models import Q, QuerySet
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from modules.core.models import Locality
from modules.initiatives.enums import InitiativeState
from modules.subscriptions.enums import EventEnum, ActiveCitizenModuleEnum
from modules.subscriptions.models import NotificationSendingLog, Subscription
from modules.subscriptions.services.mail_sending_service import (
    EmailBackendService,
)


class Subscribe(object):
    """
    Класс-декоратор для подписки на изменения в моделях
    """

    mail_service = EmailBackendService()

    event_enum = ["publish", "start", "end"]

    def __init__(self, events: List, category_field_name: str = "category"):
        self.events = self._check_events(events)
        self.category_field_name = category_field_name

    def __call__(self, func):
        """Метод-декоратор"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            instance = args[0]
            result = func(*args, **kwargs)
            self.subscribe_handler(instance)
            return result

        return wrapper

    def _check_events(self, events):
        """Проверка допустимости события"""
        assert isinstance(events, list)
        for event in events:
            assert event in self.event_enum
        return events

    @classmethod
    def _get_attr(cls, instance, attr_name: str) -> Optional[Any]:
        """Получение значения поля из объекта модели"""
        if hasattr(instance, attr_name):
            return getattr(instance, attr_name)
        return None

    @classmethod
    def _get_initiative_instance_event(cls, instance) -> str:
        """Получение события по модели Инициатива"""
        module_spec = importlib.util.find_spec("modules.initiatives.models.initiative")
        if module_spec:
            states = [
                InitiativeState.VOTES_COLLECTION,
                InitiativeState.REJECTED_VOTES_THRESHOLD,
                InitiativeState.CONSIDERATION,
                InitiativeState.IN_PROGRESS,
            ]
            events = [
                EventEnum.INITIATIVE_NEW_VOTE_START,
                EventEnum.INITIATIVE_VOTE_END,
                EventEnum.INITIATIVE_VOTE_END,
                EventEnum.DECISION_ON_INITIATIVE_PUBLICATION,
            ]
            if instance.state in states:
                return events[states.index(instance.state)]
        return ""

    def _get_instance_event(self, instance) -> str:
        """Получение события по модели"""
        model = instance.__class__
        if model.__name__ == "News":
            return self._get_news_instance_event(instance)
        elif model.__name__ == "Vote":
            return self._get_vote_instance_event(instance)
        elif model.__name__ == "Initiative":
            return self._get_initiative_instance_event(instance)
        elif model.__name__ == "Plan":
            return self._get_plan_instance_event(instance)
        elif model.__name__ == "Works":
            return self._get_map_works_instance_event(instance)
        return ""

    @classmethod
    def _get_map_works_instance_event(cls, instance) -> str:
        """Получение события по модели Работы"""
        module_spec = importlib.util.find_spec("modules.map_works.models.works")
        if module_spec:
            module = cls._import_module_from_spec(module_spec)
            module_enum = sys.modules.get("WorksState") or module.WorksState
            states = [
                module_enum.PLANNED,
                module_enum.IN_PROGRESS,
                module_enum.COMPLETED,
            ]
            events = [
                EventEnum.REPAIR_WORK_PUBLICATION,
                EventEnum.REPAIR_WORK_START,
                EventEnum.REPAIR_WORK_END,
            ]
            if instance.state in states:
                return events[states.index(instance.state)]
        return ""

    def _get_messages(self, tasks: QuerySet) -> List[EmailMessage]:
        """Формирование списка сообщений из заданий на отправку"""
        messages = []
        for task in tasks:
            messages.append(self.mail_service.message(task))
        return messages

    @classmethod
    def _get_news_instance_event(cls, instance) -> str:
        """Получение события по модели Новость"""
        events = ["", EventEnum.NEWS_PUBLICATION]
        return events[instance.is_public]

    @classmethod
    def _get_or_create_uncompleted_tasks(
        cls, subscription: Subscription
    ) -> Union[List, QuerySet, NotificationSendingLog]:
        """Выборка заданий на отправку"""
        completed_task = NotificationSendingLog.objects.filter(
            subscription=subscription, status=True
        )
        if completed_task:
            return []
        uncompleted_tasks = NotificationSendingLog.objects.filter(
            subscription=subscription, status=False
        )
        if not uncompleted_tasks:
            uncompleted_tasks = [
                NotificationSendingLog.objects.create(
                    subscription=subscription, status=False
                )
            ]
        return uncompleted_tasks

    @classmethod
    def _get_plan_instance_event(cls, instance) -> str:
        """Получение события по модели План"""
        events = ["", EventEnum.NEW_PLAN_PUBLICATION]
        return events[
            instance.publication_date.astimezone()
            <= timezone.datetime.now().astimezone()
        ]

    def _get_subscriptions(self, instance, instance_event: str) -> QuerySet:
        """Выборка подписок"""
        module = ActiveCitizenModuleEnum.get_app_by_model(instance)
        locality = self._get_attr(instance, "locality")
        category = self._get_attr(instance, self.category_field_name)
        query = Q()
        if hasattr(instance, "locality"):
            if type(locality) == Locality:
                localities_id = [locality]
            else:
                localities_id = locality.values_list('id', flat=True)
            query &= Q(locality__in=localities_id)
        query &= Q(module=module)
        query &= Q(category__icontains=category.pk)
        query &= Q(event=instance_event)
        subscriptions = Subscription.objects.filter(query).distinct()
        return subscriptions

    def _get_tasks(self, subscriptions: QuerySet) -> QuerySet:
        """Формирование заданий на отправку из подписок"""
        tasks = []
        for subscription in subscriptions:
            for task in self._get_or_create_uncompleted_tasks(subscription):
                tasks.append(task.pk)
        tasks = NotificationSendingLog.objects.filter(pk__in=tasks).distinct()
        return tasks

    @classmethod
    def _get_vote_instance_event(cls, instance) -> str:
        """Получение события по модели Голосование"""
        module_spec = importlib.util.find_spec("modules.votes.models.vote")
        if module_spec:
            module = cls._import_module_from_spec(module_spec)
            module_enum = sys.modules.get("VoteState") or module.VoteState
            states = [module_enum.PUBLISHED, module_enum.FINISHED]
            events = [EventEnum.NEW_VOTE_START, EventEnum.VOTE_END]
            if instance.state in states:
                return events[states.index(instance.state)]
        return ""

    @classmethod
    def _import_module_from_spec(cls, module_spec):
        """Динамический импорт модуля"""
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    def _send_notification(self, instance, instance_event: str) -> None:
        """Отправка сообщений"""
        subscriptions = self._get_subscriptions(instance, instance_event)
        tasks = self._get_tasks(subscriptions)
        messages = self._get_messages(tasks)
        try:
            self.mail_service.send_many(messages)
        except Exception as e:
            raise ValidationError(e)
        else:
            tasks.update(status=True)

    def subscribe_handler(self, instance):
        """Обработка подписок"""
        instance_event = self._get_instance_event(instance)
        self._send_notification(instance, instance_event)
