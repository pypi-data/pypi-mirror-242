from django.db import models

from modules.core.models import DepartmentStatus


class DepartmentCategory(models.Model):
    department = models.ForeignKey(
        to="core.Department",
        on_delete=models.CASCADE,
        verbose_name="Ведомство",
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )

    category = models.ForeignKey(
        to="appeals.Category",
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )

    def __str__(self):
        return f"{self.department} {self.category}"

    class Meta:
        verbose_name = "Категория ведомства"
        verbose_name_plural = "Категории ведомства"
        unique_together = [["department", "category"]]
