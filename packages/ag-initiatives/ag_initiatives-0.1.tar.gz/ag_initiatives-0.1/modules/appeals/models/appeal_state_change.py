import collections

from django.db import models

from modules.appeals.models import AppealState
from modules.core.models import DepartmentStatus


class AppealStateChange(models.Model):
    appeal = models.ForeignKey(
        to="appeals.Appeal",
        verbose_name="Обращение",
        on_delete=models.CASCADE,
        related_name="state_change",
    )
    new_state = models.TextField(
        choices=AppealState.CHOICES,
        verbose_name="Новый статус",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True,
    )
    second_comment = models.TextField(
        verbose_name="Комментарий",
        blank=True,
    )
    timestamp = models.DateTimeField(
        verbose_name="Дата-время изменения",
        auto_now_add=True,
    )
    user = models.ForeignKey(
        to="core.User",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    department = models.ForeignKey(
        to="core.Department",
        verbose_name="Ведомство",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )

    class Meta:
        verbose_name = "Изменение состояния обращения"
        verbose_name_plural = "Изменения состояния обращений"
