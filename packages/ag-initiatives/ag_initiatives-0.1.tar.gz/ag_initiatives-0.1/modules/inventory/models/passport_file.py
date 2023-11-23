import collections
import os

from django.db import models


class PassportFile(models.Model):
    passport = models.ForeignKey(
        to="inventory.Passport",
        verbose_name="Паспорт",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    file = models.FileField(
        verbose_name="Файл",
        upload_to="inventory",
    )

    name = models.TextField(
        verbose_name="Имя файла",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Файл схемы земельного участка"
        verbose_name_plural = "Файлы схем земельных участков"
