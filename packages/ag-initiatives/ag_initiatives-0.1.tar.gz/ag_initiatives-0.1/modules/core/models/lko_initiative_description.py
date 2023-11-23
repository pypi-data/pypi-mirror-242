import collections

from django.db import models
from modules.core.enum import InitiativeType


class LkoInitiativeDescription(models.Model):
    description_id = models.TextField(
        verbose_name="Идентификатор описания",
    )
    text = models.TextField(
        verbose_name="Текст",
        blank=True,
    )
    initiative_type = models.CharField(
        verbose_name="Тип инициативы",
        max_length=15,
        unique=True,
        choices=InitiativeType.CHOICES,
    )

    def __str__(self):
        return self.description_id

    class Meta:
        verbose_name = 'Описание механизма рассмотрения инициатив'
        verbose_name_plural = 'Описания механизмов рассмотрения инициатив'
