import collections

from django.db import models


class RejectReason(models.Model):
    text = models.TextField(
        verbose_name="Текст",
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Причина отказа"
        verbose_name_plural = "Причины отказа"
