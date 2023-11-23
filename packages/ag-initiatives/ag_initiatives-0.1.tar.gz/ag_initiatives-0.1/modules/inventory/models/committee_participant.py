from django.db import models


class CommitteeParticipant(models.Model):
    passport = models.ForeignKey(
        to="inventory.Passport",
        verbose_name="Паспорт",
        related_name="committee_participants",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    organization = models.TextField(
        verbose_name="Организация",
    )

    position = models.TextField(
        verbose_name="Должность",
    )

    last_name = models.TextField(
        verbose_name="Фамилия",
    )

    first_name = models.TextField(
        verbose_name="Имя",
    )

    patronymic_name = models.TextField(
        verbose_name="Отчество",
    )

    class Meta:
        verbose_name = "Участник инвентаризационной комисии"
        verbose_name_plural = "Участники инвентаризационных комисий"
