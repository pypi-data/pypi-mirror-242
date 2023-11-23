from django.core.validators import FileExtensionValidator
from django.db import models


class Audio(models.Model):
    title = models.CharField(max_length=255, verbose_name="Описание")
    file = models.FileField(
        verbose_name="Файл",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["webm", "mp4", "mp3", "wav", "ogg"]
            )
        ],
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Аудио"
        verbose_name_plural = "Аудио"
