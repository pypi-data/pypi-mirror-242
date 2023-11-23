import collections

from django.db import models


class PurchaseStatus(object):
    NOT_CONFIRMED = "NOT_CONFIRMED"
    CONFIRMED = "CONFIRMED"
    RETURNED = "RETURNED"
    RESOLVER = collections.OrderedDict(
        [
            (NOT_CONFIRMED, "Не подтверждено"),
            (CONFIRMED, "Подтверждено"),
            (RETURNED, "Возвращено"),
        ]
    )

    CHOICES = RESOLVER.items()


class UserPurchase(models.Model):
    user = models.ForeignKey(
        to="core.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="purchases",
    )

    goods_n_services_item = models.ForeignKey(
        to="ecology.GoodsNServicesItem",
        on_delete=models.CASCADE,
        verbose_name="Поощрение",
        related_name="purchases",
    )

    code = models.TextField(verbose_name="Код для получения поощрения")

    status = models.TextField(
        max_length=30,
        choices=PurchaseStatus.CHOICES,
        default=PurchaseStatus.NOT_CONFIRMED,
        verbose_name="Статус получения поощрения",
    )

    timestamp = models.DateTimeField(
        verbose_name="Дата-время формирования запроса", auto_now_add=True
    )

    class Meta:
        verbose_name = "Получение поощрения пользователем"
        verbose_name_plural = "Получение поощрений пользователями"
