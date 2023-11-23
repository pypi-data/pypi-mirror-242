from django.db import models


class VotingParticipant(models.Model):
    """Модель: Участник локального голосования"""

    class Meta:
        ordering = [
            "last_name",
            "first_name",
            "email",
        ]
        indexes = [models.Index(fields=["email"])]
        verbose_name = "Участник локального голосования"
        verbose_name_plural = "Участники локального голосования"

    group = models.ForeignKey(
        to="voting.LocalVotingGroup",
        verbose_name="Группа голосования",
        related_name="participants",
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )

    last_name = models.CharField(
        verbose_name="Фамилия", max_length=255, null=False, blank=False
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=255, null=False, blank=False
    )
    patronymic_name = models.CharField(
        verbose_name="Отчество", max_length=255, default=None, null=True, blank=True
    )
    email = models.EmailField(verbose_name="Электронная почта", null=False, blank=False)
    phone = models.CharField(
        verbose_name="Телефон", max_length=15, default=None, null=True, blank=True
    )
    comment = models.TextField(
        verbose_name="Комментарий", default=None, null=True, blank=True
    )

    @property
    def full_name(self):
        last_name = self.last_name or ""
        first_name = self.first_name or ""
        patronymic_name = self.patronymic_name or ""
        return f"{last_name} {first_name} {patronymic_name}"

    full_name.fget.short_description = "ФИО"

    def __str__(self):
        email = self.email or ""
        return f"{self.full_name} <{email}>"
