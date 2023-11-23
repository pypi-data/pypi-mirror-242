from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from modules.core.enum.main_page_block_type import MainPageBlockType


class MainPageBlock(models.Model):
    # block_id = models.TextField(
    #     verbose_name="Идентификатор блока",
    #     unique=True,
    # )
    # text = models.TextField(
    #     verbose_name="Текст",
    #     blank=True,
    # )
    # image = models.ForeignKey(
    #     to="core.Image",
    #     on_delete=models.SET_NULL,
    #     verbose_name="Изображение",
    #     default=None,
    #     null=True,
    #     blank=True,
    # )
    name = models.CharField(
        blank=True,
        null=True,
        choices=MainPageBlockType.CHOICES,
        max_length=30,
        verbose_name="Название"
    )
    order = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(len(MainPageBlockType.CHOICES))],
        verbose_name="Порядок"
    )

    def __str__(self):
        return self.name if self.name else ""

    class Meta:
        ordering = ['order']
        verbose_name = 'Блок главной страницы'
        verbose_name_plural = 'Блоки главной страницы'
