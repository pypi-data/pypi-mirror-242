from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from modules.core.models.settings_types import SettingsTypes


class SettingsModule(models.Model):
    """ Модель настроек модулей."""
    type = models.CharField(
        max_length=200,
        choices=[(item.name, item.value) for item in SettingsTypes],
        verbose_name="Тип настройки"
    )
    header = models.TextField(
        verbose_name="Заголовок",
    )
    text = models.TextField(
        verbose_name="Текст",
        blank=True,
    )
    image = models.ImageField(
        upload_to="images/settings",
        verbose_name="Изображение",
        blank=True,
    )
    video = models.FileField(
        upload_to="videos/settings",
        verbose_name="Видео",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["mp4", "3gp", "mpeg", "qt", "ogg", "webm"]
            )
        ],
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
        return self.header


    def clean(self):
        if self.type == SettingsTypes.PERSONAL_DATA_USAGE_POLICY.value:
            existing_objects = SettingsModule.objects.filter(type=self.type)
            if self.pk:
                if existing_objects.exclude(pk=self.pk).exists():
                    raise ValidationError("Блок с Политикой использования персональных данных уже создан")
            else:
                if existing_objects.exists():
                    raise ValidationError("Блок с Политикой использования персональных данных уже создан")


    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"
