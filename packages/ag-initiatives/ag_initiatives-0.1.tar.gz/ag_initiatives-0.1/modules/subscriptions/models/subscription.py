from django.apps import apps
from django.db import models

from modules.subscriptions.mixins import ModelTimestampsMixin
from modules.subscriptions.enums import (
    EventEnum,
    ActiveCitizenModuleEnum,
)


class Subscription(ModelTimestampsMixin):
    """Модель: Подписка"""

    class Meta:
        verbose_name = "Подписка пользователя"
        verbose_name_plural = "Подписки пользователей"
        unique_together = (
            "user",
            "event",
            "module",
            "template",
        )

    user = models.ForeignKey(
        to="core.User",
        related_name="subscriptions",
        verbose_name="Пользователь системы",
        on_delete=models.CASCADE,
    )
    locality = models.ForeignKey(
        to="core.Locality",
        related_name="subscriptions",
        verbose_name="Населенный пункт",
        on_delete=models.CASCADE,
    )
    event = models.CharField(
        verbose_name="Событие",
        choices=EventEnum.CHOICES,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )
    module = models.CharField(
        verbose_name="Модуль",
        choices=ActiveCitizenModuleEnum.CHOICES,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )
    category = models.CharField(
        verbose_name="Категория", max_length=255, help_text="модуль:Модель:pk"
    )
    template = models.ForeignKey(
        to="subscriptions.SubscriptionTemplate",
        related_name="subscriptions",
        verbose_name="Шаблон письма",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    @property
    def category_value(self):
        category = None
        try:
            category_data = self.category.split(":")
            # models = []
            model = None
            assert len(category_data) == 3
            app_models = apps.get_app_config(category_data[0]).get_models()
            for item in app_models:
                # models.append(item)
                if item.__name__ == category_data[1]:
                    model = item
                    break
            assert model

            category = model.objects.filter(pk=category_data[-1]).first()
        except AssertionError as e:
            pass

        except Exception as e:
            pass

        return category

    @property
    def event_display(self):
        return EventEnum.get(self.event)

    event_display.fget.short_description = "Событие"

    @property
    def module_display(self):
        return ActiveCitizenModuleEnum.get(self.module)

    module_display.fget.short_description = "Модуль"

    @property
    def category_display(self):
        return f"{self.category_value}"

    category_display.fget.short_description = "Категория (рубрика)"

    def __str__(self):
        category = self.category_value
        return (
            f"{self.user}: "
            f"{self.locality}/"
            f"{ActiveCitizenModuleEnum.get(self.module)}/"
            f"{EventEnum.get(self.event)}/"
            f"{category}/"
        )
