from django.db import models
from django.utils import timezone

class ActivationModerationMechanism(models.Model):
    """
    Активирует, деактивирует механизм модерации локальных голосований
    """
    active = models.BooleanField(
        verbose_name="Модерировать локальные голосования ?",
        default=True,)
    date_operation = models.DateTimeField(verbose_name="Дата операции", auto_now_add=True)

    def __str__(self):
        return f"Состояние на {self.date_operation}"
    
    class Meta:
        verbose_name = "Активация механизма модерации локальных голосований"
        verbose_name_plural = "Механизмы модерации локальных голосований"