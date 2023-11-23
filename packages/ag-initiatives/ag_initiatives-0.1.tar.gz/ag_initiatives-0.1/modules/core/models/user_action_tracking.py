from collections import OrderedDict

from django.db import models


class ActionTypeEnum(object):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    OTHER = "OTHER"

    RESOLVER = OrderedDict(
        {
            CREATE: "Добавление",
            UPDATE: "Изменение",
            DELETE: "Удаление",
            OTHER: "Прочее",
        }
    )
    CHOICES = RESOLVER.items()


class UserActionTracking(models.Model):
    """МОДЕЛЬ: ДЕЙСТВИЕ ПОЛЬЗОВАТЕЛЯ"""

    class Meta:
        verbose_name = "Действие пользователя"
        verbose_name_plural = "Действия пользователей"
        ordering = ["-timestamp"]

    timestamp = models.DateTimeField(verbose_name="Дата и время", auto_now_add=True)

    subject = models.CharField(
        verbose_name="Пользователь", default="SYSTEM", max_length=255
    )

    subject_roles = models.CharField(
        verbose_name="Роль",
        default=None,
        blank=True,
        null=True,
        max_length=1000,
    )

    subject_organization = models.CharField(
        verbose_name="Организация",
        default=None,
        blank=True,
        null=True,
        max_length=255,
    )

    module = models.CharField(
        verbose_name="Объект операции",
        default=None,
        blank=True,
        null=True,
        max_length=255,
    )

    object_name = models.CharField(
        verbose_name="Наименование объекта операции",
        default=None,
        blank=True,
        null=True,
        max_length=255,
    )

    operation_type = models.CharField(
        verbose_name="Тип операции",
        default=ActionTypeEnum.OTHER,
        choices=ActionTypeEnum.CHOICES,
        max_length=255,
    )

    locality = models.TextField(
        verbose_name="МО",
        default=None,
        blank=True,
        null=True,
        max_length=255,
    )

    value_before = models.TextField(
        verbose_name="Значение до изменений",
        default=None,
        blank=True,
        null=True,
    )

    value_after = models.TextField(
        verbose_name="Значение после изменений",
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.timestamp.astimezone().isoformat()}: {self.subject} - {self.operation_type}"
