import collections

from django.db import models


class UserState(object):
    INITIAL = "INITIAL"
    PARTICIPATE = "PARTICIPATE"
    SURVEY_SUSPEND = "SURVEY_SUSPEND"
    SURVEY_COMPLETED = "SURVEY_COMPLETED"

    RESOLVER = collections.OrderedDict(
        [
            (INITIAL, "Первоначальный"),
            (PARTICIPATE, "Принимает участие"),
            (SURVEY_SUSPEND, "Опрос отложен"),
            (SURVEY_COMPLETED, "Опрос пройден"),
        ]
    )

    CHOICES = RESOLVER.items()


class EcologyLevel(object):
    UNDEFINED = "UNDEFINED"
    HIGH = "HIGH"
    MIDDLE = "MIDDLE"
    LOW = "LOW"

    RESOLVER = collections.OrderedDict(
        [
            (UNDEFINED, "Неопределен"),
            (HIGH, "Высокий"),
            (MIDDLE, "Средний"),
            (LOW, "Низкий"),
        ]
    )

    CHOICES = RESOLVER.items()


class UserProfile(models.Model):
    user = models.OneToOneField(
        to="core.User",
        related_name="ecology_profile",
        on_delete=models.CASCADE,
    )

    state = models.TextField(
        choices=UserState.CHOICES,
        verbose_name="Состояние",
        default=UserState.INITIAL,
    )

    balance = models.IntegerField(
        verbose_name="Баланс бонусов",
        default=0,
    )

    earned_bonuses = models.IntegerField(
        verbose_name="Количество всех заработанных бонусов", default=0
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
