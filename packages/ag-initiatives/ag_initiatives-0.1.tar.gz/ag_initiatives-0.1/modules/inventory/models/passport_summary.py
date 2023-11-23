from django.db import models

from modules.core.models import DepartmentStatus


class PassportSummary(models.Model):
    year = models.PositiveIntegerField(
        verbose_name="Год",
    )

    department = models.ForeignKey(
        to="core.Department",
        verbose_name="Ведомство",
        related_name="public_territory_improvement_passport_summarrys",
        on_delete=models.CASCADE,
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )

    generation_date = models.DateField(
        verbose_name="Дата составления",
    )

    lead_last_name = models.TextField(
        verbose_name="Фамилия руководителя",
    )

    lead_first_name = models.TextField(
        verbose_name="Имя руководителя",
    )

    lead_patronymic_name = models.TextField(
        verbose_name="Отчество руководителя",
    )

    class Meta:
        verbose_name = "Сводный паспорт благоустройства общественной территории"
        verbose_name_plural = "Сводные паспорта благоустройства общественных территорий"

        unique_together = [
            ["year", "department"],
        ]
