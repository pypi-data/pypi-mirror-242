from django.core.validators import FileExtensionValidator
from django.db import models


class Image(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Описание'
    )
    file = models.FileField(
        verbose_name='Файл',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg', 'gif']
            )
        ],
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
