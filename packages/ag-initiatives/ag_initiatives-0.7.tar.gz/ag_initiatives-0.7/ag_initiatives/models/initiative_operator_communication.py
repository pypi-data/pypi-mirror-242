import collections

from django.db import models


class PremoderateChangesResponseDecision(object):
    APPROVE = "APPROVE"
    REJECT = "REJECT"

    RESOLVER = collections.OrderedDict(
        [
            (APPROVE, "Одобрить"),
            (REJECT, "Отклонить"),
        ]
    )

    CHOICES = RESOLVER.items()


class ModerateResponseState(object):
    MODERATION_REQUIRED = "MODERATION_REQUIRED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

    RESOLVER = collections.OrderedDict(
        [
            (MODERATION_REQUIRED, "Требует модерации"),
            (APPROVED, "Одобрено"),
            (REJECTED, "Отклонено"),
        ]
    )

    CHOICES = RESOLVER.items()


########################################################################################################################


class InitiativeOperatorCommunicationType(object):
    SYSTEM_NOTIFICATION = "SYSTEM_NOTIFICATION"  # text, files

    PREMODERATE_REQUEST = "PREMODERATE_REQUEST"  # text, files
    PREMODERATE_RESPONSE = "PREMODERATE_RESPONSE"  # text, files
    PREMODERATE_CHANGES_REQUEST = (
        "PREMODERATE_CHANGES_REQUEST"  # text, files, title, description, expectations
    )
    PREMODERATE_CHANGES_RESPONSE = (
        "PREMODERATE_CHANGES_RESPONSE"  # decision(PremoderateChangesResponseDecision)
    )
    PREMODERATE_REJECT = "PREMODERATE_REJECT"  # text, files
    PREMODERATE_APPROVE = "PREMODERATE_APPROVE"

    MODERATE_REQUEST = "MODERATE_REQUEST"  # text, files
    MODERATE_RESPONSE = "MODERATE_RESPONSE"  # text, files, state(ModerateResponseState)
    MODERATE_REJECT = "MODERATE_REJECT"  # text, files
    MODERATE_APPROVE = "MODERATE_APPROVE"  # text, files

    IN_PROGRESS_NOTIFICATION = "IN_PROGRESS_NOTIFICATION"  # text, files
    ACCOMPLISHED_NOTIFICATION = "ACCOMPLISHED_NOTIFICATION"  # text, files

    RESOLVER = collections.OrderedDict(
        [
            (SYSTEM_NOTIFICATION, "Сообщение системы"),
            (PREMODERATE_REQUEST, "Запрос модератора"),
            (PREMODERATE_RESPONSE, "Ответ на запрос модератора"),
            (PREMODERATE_CHANGES_REQUEST, "Запрос модератора на изменение инициативы"),
            (
                PREMODERATE_CHANGES_RESPONSE,
                "Ответ пользователя на изменение инициативы",
            ),
            (PREMODERATE_REJECT, "Инициатива отклонена по решению модератора"),
            (PREMODERATE_APPROVE, "Инициатива одобрена модератором"),
            (MODERATE_REQUEST, "Запрос оператора"),
            (MODERATE_RESPONSE, "Ответ на запрос оператора"),
            (MODERATE_REJECT, "Инициатива отклонена по решению оператора"),
            (MODERATE_APPROVE, "Инициатива опубликована по решению оператора"),
            (IN_PROGRESS_NOTIFICATION, "Решение о реализации инициативы"),
            (ACCOMPLISHED_NOTIFICATION, "Результаты реализации инициативы"),
        ]
    )

    CHOICES = RESOLVER.items()


########################################################################################################################


class InitiativeOperatorCommunication(models.Model):
    initiative = models.ForeignKey(
        to="initiatives.Initiative",
        related_name="initiative_operator_communication",
        verbose_name="Инициатива",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to="core.User",
        verbose_name="Отправитель",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(
        verbose_name="Дата-время",
    )
    type = models.TextField(
        choices=InitiativeOperatorCommunicationType.CHOICES,
        verbose_name="Тип",
    )

    text = models.TextField(
        verbose_name="Текст",
        null=True,
        blank=True,
    )
    files = models.ManyToManyField(
        to="initiatives.InitiativeFile",
        verbose_name="Файлы",
        blank=True,
    )

    title = models.TextField(
        verbose_name="Заголовок",
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True,
    )
    expectations = models.TextField(
        verbose_name="Ожидаемый результат",
        null=True,
        blank=True,
    )

    decision = models.TextField(
        verbose_name="Решение",
        choices=PremoderateChangesResponseDecision.CHOICES,
        null=True,
        blank=True,
    )

    state = models.TextField(
        verbose_name="Состояние",
        choices=ModerateResponseState.CHOICES,
        null=True,
        blank=True,
    )

    user_viewed = models.BooleanField(
        verbose_name="Просмотрено пользователем",
        default=False,
    )
    moderator_viewed = models.BooleanField(
        verbose_name="Просмотрено модератором",
        default=False,
    )
    operator_viewed = models.BooleanField(
        verbose_name="Просмотрено оператором",
        default=False,
    )

    class Meta:
        verbose_name = "Коммуникация c пользователем"
        verbose_name_plural = "Коммуникация c пользователем"
