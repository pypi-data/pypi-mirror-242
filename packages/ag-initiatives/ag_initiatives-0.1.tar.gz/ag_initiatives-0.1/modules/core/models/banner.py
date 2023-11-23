from django.db import models


class Banner(models.Model):
    title = models.TextField(blank=True, default="", verbose_name="Заголовок")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    url = models.URLField(verbose_name="Ссылка")
    url_title = models.TextField(verbose_name="Заголовок ссылки")
    image = models.ImageField(
        upload_to="images/banners",
        verbose_name="Баннер",
        help_text="(максимальный размер файла 5 МБ)",
    )

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

    def __str__(self):
        return self.title if len(self.title) else "Баннер"
