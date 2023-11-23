from django.db import models


class ModelTimestampsMixin(models.Model):
    """
    Миксин для моделей базы данных - добавляет временные метки к моделям
    Очередь использования - в конце
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )

    class Meta:
        abstract = True
