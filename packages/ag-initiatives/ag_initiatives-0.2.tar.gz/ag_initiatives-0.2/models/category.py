from django.db import models


class InitiativeCategory(models.Model):
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Родительская категория",
        related_name="children",
    )
    name = models.TextField(verbose_name="Наименование")
    color = models.CharField(
        verbose_name="Цвет html",
        default="#000000",
        max_length=7,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 5 МБ)",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тематическая категория"
        verbose_name_plural = "Тематические категории"
