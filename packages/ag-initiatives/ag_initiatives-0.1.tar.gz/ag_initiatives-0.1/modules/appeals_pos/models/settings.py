import datetime

from django.db import models

from modules.core.models.settings import SingletonModel


class Settings(SingletonModel):
    appeals_rules = models.TextField(
        blank=True, null=True, verbose_name="Правила подачи обращений"
    )

    default_category_image = models.ImageField(
        blank=True, null=True, verbose_name="Картинка для категорий по умолчанию"
    )
    update_time = models.TimeField(
        default=datetime.time(hour=0, minute=0),
        verbose_name="Ежедневное время обновления данных из ПОС",
        editable=False,
    )

    def __str__(self):
        return "Настройки"

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"
