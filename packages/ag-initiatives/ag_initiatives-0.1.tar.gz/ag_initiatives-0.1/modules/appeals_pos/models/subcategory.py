from django.db import models


class Subcategory(models.Model):
    category = models.ForeignKey(
        to="appeals_pos.Category",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="subcategories",
        verbose_name="Категория",
    )
    pos_id = models.IntegerField(unique=True, verbose_name="Идентификатор ПОС")
    name = models.CharField(max_length=500, verbose_name="Наименование")
    deleted = models.BooleanField(default=False, verbose_name="Удалено")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
