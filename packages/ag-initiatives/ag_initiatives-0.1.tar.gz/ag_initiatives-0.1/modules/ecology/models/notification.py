import collections
import os

from django.db import models

from modules.ecology.models import EcologyLevel


class NotificationType(object):
    PARTICIPATE = "PARTICIPATE"
    SURVEY_COMPLETED = "SURVEY_COMPLETED"
    EVENT_PARTICIPATION = "EVENT_PARTICIPATION"
    DECLINE_EVENT_PARTICIPATION = "DECLINE_EVENT_PARTICIPATION"
    GOODSNSERVICES_PURCHASE = "GOODSNSERVICES_PURCHASE"
    RETURN_GOODSNSERVICES_PURCHASE = "RETURN_GOODSNSERVICES_PURCHASE"
    ADDING_INITIATIVE = "ADDING_INITIATIVE"
    APPROVE_INITIATIVE = "APPROVE_INITIATIVE"
    VOTING_PARTICIPATION = "VOTING_PARTICIPATION"
    EXTERNAL_REDUCTION = "EXTERNAL_REDUCTION"
    EXTERNAL_INCREASE = "EXTERNAL_INCREASE"

    RESOLVER = collections.OrderedDict(
        [
            (PARTICIPATE, "Принято участие в проекте"),  # начисление
            (SURVEY_COMPLETED, "Заполнена анкета"),  # начисление
            (EVENT_PARTICIPATION, "Принято участие в мероприятии"),  # начисление
            (DECLINE_EVENT_PARTICIPATION, "Отклонено участие в предложении"),
            (GOODSNSERVICES_PURCHASE, "Совершена покупка поощрения"),
            (RETURN_GOODSNSERVICES_PURCHASE, "Произведен возврат поощрения"),  # начисление
            (ADDING_INITIATIVE, "Предложена инициатива"),  # начисление
            (APPROVE_INITIATIVE, "Поддержана инициатива"),  # начисление
            (VOTING_PARTICIPATION, "Принято участие в голосовании"),  # начисление
            (EXTERNAL_REDUCTION, "Уменьшение баланса во внешней системе"),
            (EXTERNAL_INCREASE, "Увеличение баланса во внешней системе"),  # начисление
        ]
    )

    CHOICES = RESOLVER.items()


class Notification(models.Model):
    user = models.ForeignKey(
        to="core.User",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    timestamp = models.DateTimeField(
        verbose_name="Дата-время",
    )

    text = models.TextField(
        verbose_name="Сообщение",
    )

    type = models.TextField(
        choices=NotificationType.CHOICES,
        verbose_name="Тип",
    )

    user_balance_operation = models.ForeignKey(
        to="ecology.UserBalanceOperation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        verbose_name="Операция с балансом",
    )

    participation = models.ForeignKey(
        to="ecology.ParticipationUserEvent",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Участие в мероприятии",
    )

    user_purchase = models.ForeignKey(
        to="ecology.UserPurchase",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Покупка",
    )

    initiative = models.ForeignKey(
        to="initiatives.Initiative",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Инициатива",
    )

    vote = models.ForeignKey(
        to="voting.Vote",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Голосование",
    )
    target = models.TextField(
        verbose_name="Предмет начисления или списания бонусов",
        null=True,
        blank=True,
    )

    class Meta:
        """Это уведомления, но в админке по тз требуется название операции"""

        verbose_name = "Операция"
        verbose_name_plural = "Операции"
