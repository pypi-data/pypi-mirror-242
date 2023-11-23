import collections

from django.contrib.postgres.fields import ArrayField
from django.db import models


class AppealAnswerType:
    POSTPONED = "POSTPONED"
    NOT_SOLVED = "NOT_SOLVED"
    SOLVED = "SOLVED"
    REJECTED = "REJECTED"

    RESOLVER = collections.OrderedDict(
        [
            (POSTPONED, "Отложено"),
            (NOT_SOLVED, "Не решено"),
            (SOLVED, "Решено"),
            (REJECTED, "Отклонено"),
        ]
    )

    CHOICES = RESOLVER.items()


class AppealAnswer(models.Model):
    appeal_state_change = models.OneToOneField(
        to="appeals_pos.AppealStateChange",
        on_delete=models.CASCADE,
        verbose_name="Изменение состояния обращения",
        related_name="answer",
    )
    answer_type = models.CharField(
        max_length=50, verbose_name="Тип ответа", choices=AppealAnswerType.CHOICES
    )
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    reject_reason = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Причина отказа"
    )
    files = ArrayField(
        base_field=models.TextField(),
        verbose_name="Ссылки на файлы",
        null=True, blank=True,
    )

    @property
    def answer_type_name(self):
        return AppealAnswerType.RESOLVER.get(self.answer_type, None)

    def __str__(self):
        return f'{self.appeal_state_change.__str__()} {self.answer_type_name if self.answer_type_name else ""}'

    class Meta:
        verbose_name = "Ответ обращение"
        verbose_name_plural = "Ответы на обращения"
