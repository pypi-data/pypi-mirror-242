from django.core.validators import FileExtensionValidator
from django.db import models


class InformationalMessages(models.Model):
    """ Модель информационных сообщений."""
    header = models.TextField(
        verbose_name="Название информационного сообщения",
        blank=True,
    )
    text = models.TextField(
        max_length=500,
        verbose_name="Текст",
    )
    image = models.ImageField(
        upload_to="images/informational_messages",
        verbose_name="Изображение",
        blank=True,
    )
    link_title = models.CharField(
        max_length=100,
        verbose_name="Заголовок ссылки",
        blank=True,
    )
    link = models.URLField(
        verbose_name="Ссылка",
        blank=True,
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Информационное сообщение"
        verbose_name_plural = "Информационные сообщения"
