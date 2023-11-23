from django.db import models

from modules.core.models import DepartmentStatus


class AppealResponse(models.Model):
    appeal = models.OneToOneField(
        to="appeals.Appeal",
        related_name="response",
        verbose_name="Обращение",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to="core.User",
        verbose_name="Отправитель",
        on_delete=models.CASCADE,
    )
    department = models.ForeignKey(
        to="core.Department",
        verbose_name="Ведомство",
        on_delete=models.CASCADE,
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )
    timestamp = models.DateTimeField(
        verbose_name="Дата-время",
    )

    text = models.TextField(
        verbose_name="Текст",
    )
    files = models.ManyToManyField(
        to="appeals.File",
        verbose_name="Файлы",
        blank=True,
    )

    class Meta:
        verbose_name = "Ответ на обращение"
        verbose_name_plural = "Ответы на обращения"
