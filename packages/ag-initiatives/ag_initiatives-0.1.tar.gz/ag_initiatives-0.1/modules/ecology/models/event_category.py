from django.db import models


class EventCategory(models.Model):
    name = models.TextField(verbose_name="Наименование")

    color = models.CharField(
        verbose_name="Цвет html",
        default="#000000",
        max_length=7,
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to="ecology",
        verbose_name="Изображение",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 5 МБ)",
    )

    icon = models.FileField(
        upload_to="ecology",
        verbose_name="Иконка",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 5 МБ)",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория предложения"
        verbose_name_plural = "Категории предложений"

        ordering = ["name"]
