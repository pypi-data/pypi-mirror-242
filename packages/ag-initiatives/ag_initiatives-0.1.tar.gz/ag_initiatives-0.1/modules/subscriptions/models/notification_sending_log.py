from django.db import models


class NotificationSendingLog(models.Model):
    """Модель: Журнал отправки почты"""

    class Meta:
        verbose_name = "Запись об отправке оповещения"
        verbose_name_plural = "Журнал отправки оповещений"
        ordering = [
            "timestamp",
        ]

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
    status = models.BooleanField(verbose_name="Статус отправки", default=False)
    subscription = models.ForeignKey(
        to="subscriptions.Subscription",
        related_name="mail_sending_journal",
        verbose_name="Подписка",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        user = str(self.subscription.user)
        timestamp = self.timestamp.astimezone().isoformat()
        status = "Отправлено" if self.status else "Не отправлено"
        return f"{self.id} - {user} - {timestamp} - {status}"
