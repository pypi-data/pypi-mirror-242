from django.db import models


class Category(models.Model):
    """
    Категория голосования.
    В категиории находится негораниченное количество голосований.
    Пример "Благоустройство дворов"
    """

    name = models.TextField(verbose_name="Рубрика голосований")
    color = models.CharField(
        verbose_name="Цвет html",
        default="#000000",
        max_length=7,
    )
    images = models.ManyToManyField(
        to="core.File",
        verbose_name="Изображения",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рубрика"
        verbose_name_plural = "Рубрики"

        ordering = ["name"]
