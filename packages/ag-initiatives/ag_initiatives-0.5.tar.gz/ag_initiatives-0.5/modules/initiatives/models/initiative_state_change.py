import collections

from django.db import models

from modules.initiatives.models import InitiativeState


class InitiativeStateChange(models.Model):
    initiative = models.ForeignKey(
        to="initiatives.Initiative",
        verbose_name="Инициатива",
        on_delete=models.CASCADE,
    )
    new_state = models.TextField(
        choices=InitiativeState.CHOICES,
        verbose_name="Новый статус",
    )
    timestamp = models.DateTimeField(
        verbose_name="Дата-время изменения",
    )
    user = models.ForeignKey(
        to="core.User",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Изменение состояния инициативы"
        verbose_name_plural = "Изменения состояния инициатив"
