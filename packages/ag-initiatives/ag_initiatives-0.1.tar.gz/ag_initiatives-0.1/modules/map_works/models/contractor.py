from django.db import models


class Contractor(models.Model):
    name = models.TextField(
        verbose_name="Наименование",
    )

    contacts = models.TextField(
        verbose_name="Контактные данные",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подрядчик"
        verbose_name_plural = "Подрядчики"
