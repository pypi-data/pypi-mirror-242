from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework import serializers


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name="Описание", blank=True, null=True)
    file = models.FileField(
        verbose_name="Файл",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "3gp", "mpeg", "qt", "ogg", "webm"]
            )
        ],
    )

    def __str__(self):
        return str(self.title) if self.title else 'Видео'

    @property
    def link_from_model(self):
        if self.file:
            return serializers.FileField().to_representation(self.file)
        return ""

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
