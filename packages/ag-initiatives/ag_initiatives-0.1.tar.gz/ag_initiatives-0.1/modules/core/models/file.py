import collections

from rest_framework import serializers
from django.db import models


class FileType(object):
    IMAGE = "IMAGE"
    DOCUMENT = "DOCUMENT"

    RESOLVER = collections.OrderedDict(
        [
            (IMAGE, "Изображение"),
            (DOCUMENT, "Документ"),
        ]
    )

    CHOICES = RESOLVER.items()


class File(models.Model):
    file = models.FileField(
        verbose_name="Файл",
    )
    type = models.TextField(
        choices=FileType.CHOICES,
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
        related_name="core_files",
    )

    def __str__(self):
        return f"{self.name} {FileType.RESOLVER.get(self.type)}"

    @property
    def link_from_model(self):
        if self.file:
            return serializers.FileField().to_representation(self.file)
        return ""

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
