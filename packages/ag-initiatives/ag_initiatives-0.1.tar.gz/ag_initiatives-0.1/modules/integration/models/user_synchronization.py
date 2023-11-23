from django.db import models


class UserSynchronization(models.Model):
    user = models.ForeignKey(
        verbose_name="пользователь",
        to="core.User",
        related_name="user_synchronization",
        on_delete=models.CASCADE
    )
    external_system = models.ForeignKey(
        verbose_name="внешняя ИС",
        to="integration.ExternalSystemToken",
        related_name="user_synchronization",
        on_delete=models.CASCADE
    )
    synchorized_user_id = models.TextField(verbose_name="id пользователя во внешней системе")
    synchonization_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "синхронизация пользователя"
        verbose_name_plural = "синхронизации пользователей"
        unique_together = ("user", "synchorized_user_id", "external_system")

    def __str__(self):
        return f"{self._meta.verbose_name} №{self.pk}"
