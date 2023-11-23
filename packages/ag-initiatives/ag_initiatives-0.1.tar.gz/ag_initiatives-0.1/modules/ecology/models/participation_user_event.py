from enum import Enum
from io import BytesIO
import collections

from django.db import models
import qrcode.image.svg
import qrcode


class ParticipationStatus(object):

    NOT_CONFIRMED = "NOT_CONFIRMED"
    CONFIRMED = "CONFIRMED"
    DECLINED = "DECLINED"
    RESOLVER = collections.OrderedDict(
        [
            (NOT_CONFIRMED, "Не подтверждено"),
            (CONFIRMED, "Подтверждено"),
            (DECLINED, "Отклонено"),
        ]
    )

    CHOICES = RESOLVER.items()


class ParticipationUserEvent(models.Model):
    participant = models.ForeignKey(
        to="core.User",
        on_delete=models.CASCADE,
        verbose_name="Участник",
        related_name="participation_user_event_participant",
    )

    event = models.ForeignKey(
        to="ecology.Event",
        on_delete=models.CASCADE,
        verbose_name="Мероприятие",
        related_name="participation_user_event_event",
    )

    timestamp = models.DateTimeField(
        verbose_name="Дата-время запроса на подтверждение", auto_now_add=True
    )

    confirmation_timestamp = models.DateTimeField(
        verbose_name="Дата-Время подтверждения или отклонения запроса",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        verbose_name="Статус участия",
        choices=ParticipationStatus.CHOICES,
        default="NOT_CONFIRMED",
    )

    class Meta:
        verbose_name = "Участие пользователя в мероприятии"
        verbose_name_plural = "Участие пользователей в мероприятиях"
        indexes = [
            models.Index(fields=["participant", "event"]),
        ]

    # @property
    # def svg_qrcode(self):
    #     factory = qrcode.image.svg.SvgImage
    #     stream = BytesIO()
    #     data = 'link'
    #     img = qrcode.make(data, image_factory=factory)
    #     img.save(stream)
    #     qrcode_svg = stream.getvalue().decode()
    #     stream.close()
    #     return qrcode_svg
