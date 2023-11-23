import collections

from django.db import models


class AppealOwnerCommunicationType(object):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"

    RESOLVER = collections.OrderedDict(
        [
            (REQUEST, "Запрос"),
            (RESPONSE, "Ответ"),
        ]
    )

    CHOICES = RESOLVER.items()


class AppealOwnerCommunications(models.Model):
    appeal = models.ForeignKey(
        to="appeals.Appeal",
        verbose_name="Обращение",
        on_delete=models.CASCADE,
        related_name="owner_communications",
    )
    timestamp = models.DateTimeField(
        verbose_name="Дата-время",
    )
    text = models.TextField(
        verbose_name="Текст",
        null=True,
        blank=True,
    )
    files = models.ManyToManyField(
        to="appeals.File",
        verbose_name="Файлы",
        blank=True,
    )
    type = models.TextField(
        choices=AppealOwnerCommunicationType.CHOICES,
        verbose_name="Тип",
    )

    class Meta:
        verbose_name = "Общение с владельцем обращения"
        verbose_name_plural = "Общение с владельцами обращений"
