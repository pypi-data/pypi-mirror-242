from django.db import models


class PlanComment(models.Model):
    plan = models.ForeignKey(
        to="plans.Plan",
        verbose_name="План",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    text = models.TextField(
        verbose_name="Текст",
    )

    timestamp = models.DateTimeField(
        verbose_name="Дата-время",
    )

    user = models.ForeignKey(
        to="core.User",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    moderated = models.BooleanField(
        verbose_name="Модерация пройдена",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        # unique_together = [['plan', 'user']]
