from django.db import models


class UserInitiativeApprove(models.Model):
    user = models.ForeignKey(
        to="core.User",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    initiative = models.ForeignKey(
        to="initiatives.Initiative",
        related_name="user_initiative_approve",
        verbose_name="Инициатива",
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата-время",
    )

    class Meta:
        verbose_name = "Одобрение пользователем"
        verbose_name_plural = "Одобрения пользователей"
        unique_together = [["user", "initiative"]]
