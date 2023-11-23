import collections

from django.db import models


class UserBalanceOperationType(object):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

    RESOLVER = collections.OrderedDict(
        [
            (INCOME, "Зачисление"),
            (EXPENSE, "Списание"),
        ]
    )

    CHOICES = RESOLVER.items()


class UserBalanceOperation(models.Model):
    user = models.ForeignKey(
        to="core.User",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    timestamp = models.DateTimeField(
        verbose_name="Дата-время операции",
    )

    type = models.TextField(
        verbose_name="Тип",
        choices=UserBalanceOperationType.CHOICES,
    )

    amount = models.PositiveIntegerField(
        verbose_name="Количество",
    )

    participation = models.ForeignKey(
        to="ecology.ParticipationUserEvent",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Участие в предложении",
    )

    purchase = models.ForeignKey(
        to="ecology.UserPurchase",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Получение поощрения",
    )

    reason = models.TextField(
        verbose_name="Причина",
    )
    target = models.TextField(
        verbose_name="Предмет начисления или списания бонусов",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Операция баланса пользователя"
        verbose_name_plural = "Операции баланса пользователя"
