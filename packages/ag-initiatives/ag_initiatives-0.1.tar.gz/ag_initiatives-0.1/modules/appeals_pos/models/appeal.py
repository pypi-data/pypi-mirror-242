import collections
from dataclasses import dataclass

from django.db import models


@dataclass
class Coordinates:
    latitude: float
    longitude: float

    def __str__(self):
        return f"{self.latitude},{self.longitude}"


class SmevState(object):
    PREPARING = "PREPARING"
    SMEV_ERR = "SMEV_ERR"
    WAITING_RESPONSE = "WAITING_RESPONSE"
    SUCCESS = "SUCCESS"

    RESOLVER = collections.OrderedDict(
        [
            (PREPARING, "Подготовка к отправке в ПОС"),
            (SMEV_ERR, "Ошибка при отправке в ПОС"),
            (WAITING_RESPONSE, "Ожидание ответа от ПОС"),
            (SUCCESS, "Обращение зарегистрировано в ПОС"),
        ]
    )
    CHOICES = RESOLVER.items()


class AppealState(object):
    MODERATION = "MODERATION"
    MODERATION_ACCEPTED = "MODERATION_ACCEPTED"
    MODERATION_REJECTED = "MODERATION_REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    RESPONDED = "RESPONDED"

    RESOLVER = collections.OrderedDict(
        [
            (MODERATION, "На модерации"),
            (MODERATION_REJECTED, "Отклонено"),
            (MODERATION_ACCEPTED, "На рассмотрении"),
            (IN_PROGRESS, "В работе"),
            (RESPONDED, "Получен ответ"),
        ]
    )

    POS_MAPPING = {
        "MODERATION_NEW": MODERATION,
        "SEND_RESPONSE": RESPONDED,
        "MODERATION_DECLINE": MODERATION_REJECTED,
        "TAKE_TO_WORK": IN_PROGRESS,
        "FORWARD_TO_PARENT": MODERATION_ACCEPTED,
        "FORWARD_TO_SUBORDINATE": MODERATION_ACCEPTED,
        "POSTPONE": IN_PROGRESS,
        "SET_EXECUTOR": IN_PROGRESS,
        "MODERATION_ACCEPT": MODERATION_ACCEPTED,
    }

    @classmethod
    def from_pos_status(cls, pos_status: str) -> str:
        return cls.POS_MAPPING.get(pos_status)

    CHOICES = RESOLVER.items()


class Appeal(models.Model):
    pos_id = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Идентификатор ПОС"
    )
    user = models.ForeignKey(
        to="core.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="appeals",
    )
    text = models.TextField(verbose_name="Текст обращения")
    subcategory = models.ForeignKey(
        to="appeals_pos.Subcategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Подкатегория",
        related_name='appeals',
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=30,
        choices=AppealState.CHOICES,
        default=AppealState.MODERATION,
    )
    smev_status = models.CharField(
        verbose_name="Статус сообщения СМЭВ",
        max_length=30,
        choices=SmevState.CHOICES,
        default=SmevState.PREPARING,
    )
    locality = models.ForeignKey(
        to="core.Locality",
        verbose_name="Муниципальное образование",
        on_delete=models.CASCADE,
        related_name="appeals",
        null=True,
        blank=False,
    )
    creation_date_time = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    address = models.TextField(
        verbose_name="Адрес",
    )
    coordinates = models.CharField(
        max_length=100,
        verbose_name="Координаты",
        blank=True, null=True,
    )
    files = models.ManyToManyField(
        to="appeals_pos.File",
        verbose_name="Приложения",
        related_name="appeals",
        blank=True,
    )
    to_publish = models.BooleanField(
        default=True, verbose_name="Согласие публикации на портале"
    )

    def object_coordinates(self):
        if not self.coordinates:
            return None
        try:
            coordinates = self.coordinates.split(",")
            return Coordinates(
                latitude=float(coordinates[0]), longitude=float(coordinates[1])
            )
        except Exception:
            return None

    def __str__(self):
        return f'[{self.pos_id}] {self.user} {self.creation_date_time.date()} {self.creation_date_time.strftime("%H:%M")}'

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
