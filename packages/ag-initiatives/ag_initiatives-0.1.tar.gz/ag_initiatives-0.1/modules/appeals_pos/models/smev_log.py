from django.db import models


class SmevLog(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )
    description = models.CharField(
        max_length=100,
        verbose_name='Описание',
        default="",
    )
    xml_data = models.TextField(
        verbose_name='Данные',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Лог ответов СМЭВ'
        verbose_name_plural = 'Лог ответов СМЭВ'
