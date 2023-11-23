from django.db import models


class Category(models.Model):
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Родительская категория",
        related_name="children",
    )
    name = models.TextField(verbose_name="Наименование")
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )
    color = models.CharField(
        verbose_name="Цвет html",
        default="#000000",
        max_length=7,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="plans",
        verbose_name="Изображение",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 5 МБ)",
    )
    icon = models.FileField(
        upload_to="plans",
        verbose_name="Иконка",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 5 МБ)",
    )
    icon_color = models.CharField(
        verbose_name="Цвет иконки",
        default="#000000",
        max_length=7,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
