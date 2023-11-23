from collections import OrderedDict

from django.db import models
from django.utils import timezone

from .problematic import Problematic
from .objecttype import ObjectType
from .qrgenerator import QRGenerator


class OpinionStatus(object):
    NEW = "NEW"
    UNDER_CONSIDERATION = "UNDER_CONSIDERATION"
    IN_WORK = "IN_WORK"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESPONSE_SENT = "RESPONSE_SENT"

    RESOLVER = OrderedDict(
        [
            (NEW, "Новое"),
            (UNDER_CONSIDERATION, "На рассмотрении"),
            (IN_WORK, "В работе"),
            (UNDER_REVIEW, "На проверке"),
            (RESPONSE_SENT, "Направлен ответ"),
        ]
    )

    CHOICES = RESOLVER.items()


class Opinion(models.Model):

    user = models.ForeignKey(
        to="core.User",
        verbose_name="Отправитель",
        related_name="opinions",
        on_delete=models.CASCADE,
    )

    object_type = models.ForeignKey(
        ObjectType,
        verbose_name="Тип объекта",
        related_name="opinions",
        on_delete=models.CASCADE,
    )

    object_name = models.CharField(
        verbose_name="Название объекта",
        null=True,
        blank=True,
        max_length=300,
    )

    object_address = models.TextField(
        verbose_name="Адрес объекта",
        null=True,
        blank=True,
    )

    email_of_responsible_person = models.EmailField(
        verbose_name="Электронный адрес ответственного лица",
        null=True,
        blank=True,
        max_length=100,
    )

    text = models.TextField(verbose_name="Текст мнения", null=True, blank=True)

    problematic = models.ForeignKey(
        Problematic,
        verbose_name="Проблематика",
        related_name="opinions",
        on_delete=models.CASCADE,
    )

    placement_date = models.DateTimeField(
        verbose_name="Дата размещения", auto_now_add=True
    )

    status = models.CharField(
        choices=OpinionStatus.CHOICES,
        verbose_name="Статус",
        max_length=100,
        default=OpinionStatus.RESOLVER["NEW"],
    )

    user_phone = models.CharField(
        verbose_name="Номер телефона пользователя",
        blank="True",
        max_length=20,
    )

    user_email = models.CharField(
        verbose_name="Электронный адрес пользователя",
        null=True,
        blank=True,
        max_length=100,
    )
    uploaded_image = models.ForeignKey(
        to="core.File",
        null=True,
        verbose_name="Загруженное изображение",
        related_name="opinions",
        on_delete=models.CASCADE,
    )

    last_modified_date = models.DateTimeField(
        verbose_name="Дата последнего изменения", auto_now=True
    )
    locality = models.ManyToManyField(
        to="core.Locality",
        blank=True,
        verbose_name="Муниципальные образования",
        related_name='opinions',
    )

    @property
    def number(self):
        num_mask = "О-000000000"
        opinion_id = str(self.id)
        number = num_mask[0 : len(num_mask) - len(opinion_id)] + opinion_id
        return number

    def __str__(self):
        return f"{self.user} - {self.email_of_responsible_person}"

    class Meta:
        verbose_name = "Мнение"
        verbose_name_plural = "Мнения"

        indexes = [
            models.Index(
                fields=[
                    "id",
                ]
            ),
        ]
