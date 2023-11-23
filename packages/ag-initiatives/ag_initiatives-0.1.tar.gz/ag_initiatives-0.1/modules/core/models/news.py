from django.db import models

from modules.subscriptions.mixins.subscribe_mixin import SubscribeMixin
from embed_video.fields import EmbedVideoField


class News(SubscribeMixin, models.Model):
    title = models.TextField(verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое описание")
    category = models.ForeignKey(
        to="core.Category", verbose_name="Категория", on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="images/news/",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="(максимальный размер файла 5 МБ)",
    )
    text = models.TextField(verbose_name="Текст новости")
    url = models.URLField(
        verbose_name="Ссылка на новость",
        blank=True,
        null=True,
    )
    url_title = models.TextField(
        verbose_name="Текст ссылки",
    )
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    video = models.ForeignKey(
        to="core.Video",
        on_delete=models.SET_NULL,
        verbose_name="Видео",
        default=None,
        null=True,
        blank=True,
    )
    audio = models.ForeignKey(
        to="core.Audio",
        on_delete=models.SET_NULL,
        verbose_name="Аудио",
        default=None,
        null=True,
        blank=True,
    )
    is_public = models.BooleanField(
        default=True, verbose_name="Опубликовано на портале"
    )

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title if len(self.title) else "Новость"
