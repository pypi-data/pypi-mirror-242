from django.db import models


class InstitutionType(models.Model):
    name = models.TextField(
        verbose_name="Наименование",
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип учреждения"
        verbose_name_plural = "Типы учреждений"
