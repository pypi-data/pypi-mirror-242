from django.db import models


class Category(models.Model):
    pos_id = models.IntegerField(unique=True, verbose_name="Идентификатор ПОС")
    name = models.CharField(max_length=500, verbose_name="Наименование")
    deleted = models.BooleanField(default=False, verbose_name="Удалено")
    color = models.CharField(
        verbose_name="Цвет html",
        default="#000000",
        max_length=7,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="appeals_pos",
        verbose_name="Изображение",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 5 МБ)",
    )
    icon = models.FileField(
        upload_to="appeals",
        verbose_name="Иконка",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 5 МБ)",
    )
    fact_id = models.IntegerField(
        verbose_name="ID факта",
        null=True,
        blank=True,
    )
    fact = models.TextField(
        verbose_name="факт",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
