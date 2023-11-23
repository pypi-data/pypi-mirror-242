from django.db import models


class Survey(models.Model):
    name = models.TextField(
        verbose_name="Наименование",
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )

    timestamp_add = models.DateTimeField(
        verbose_name="Дата-время создания",
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Анкета"
        verbose_name_plural = "Анкеты"
