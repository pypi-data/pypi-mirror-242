import collections
import os

from django.db import models


class InitiativeFileType(object):
    IMAGE = "IMAGE"
    DOCUMENT = "DOCUMENT"

    RESOLVER = collections.OrderedDict(
        [
            (IMAGE, "Изображение"),
            (DOCUMENT, "Документ"),
        ]
    )

    CHOICES = RESOLVER.items()


class InitiativeFile(models.Model):
    file = models.FileField(
        verbose_name="Файл",
        upload_to="initiatives",
    )
    type = models.TextField(
        choices=InitiativeFileType.CHOICES,
        verbose_name="Тип файла",
    )
    name = models.TextField(
        verbose_name="Имя файла",
    )
    order = models.PositiveIntegerField(
        verbose_name="Порядок",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        to="core.User",
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
