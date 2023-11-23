from django.db import models

from modules.appeals_pos.models.appeal import AppealState


class AppealStateChange(models.Model):
    appeal = models.ForeignKey(
        to="appeals_pos.Appeal",
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name="Обращение",
    )
    status = models.CharField(
        max_length=50, choices=AppealState.CHOICES, verbose_name="Статус"
    )
    pos_status = models.CharField(
        verbose_name="Статус ПОС", max_length=50, null=True, blank=True
    )
    pos_status_name = models.CharField(
        verbose_name="Название статуса ПОС", max_length=255, null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name="Дата добавления")
    created_by = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Кем создано"
    )
    is_hide = models.BooleanField(
        verbose_name="Статус скрыт",
        default=False,
    )

    def __str__(self):
        return f"{self.appeal.__str__()} {self.created_at} {self.status}"

    class Meta:
        verbose_name = "Изменение состояния обращения"
        verbose_name_plural = "Изменения состояний обращений"
