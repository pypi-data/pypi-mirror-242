from django.db import models

from .vote_answer_option import AnswerOptionType


class VoteMunicipalAnswer(models.Model):
    """
    Вопрос голосования.
    Пример "Какой двор Вы бы хотели видеть благоустроенным к 2021 году?"
    """

    vote_question = models.ForeignKey(
        to="voting.VoteMunicipalQuestion",
        related_name="municipal_answers",
        on_delete=models.CASCADE,
        verbose_name="Вопрос голосования",
    )
    brief = models.TextField(
        default="", verbose_name="Краткое описание варианта ответа"
    )
    description = models.TextField(
        blank=True, default="", verbose_name="Полное описание варианта ответа"
    )
    image = models.ForeignKey(
        null=True,
        blank=True,
        verbose_name="Вспомогательное изображение",
        help_text="(максимальный размер файла 5 МБ)",
        to="core.File",
        on_delete=models.CASCADE,
        related_name="vote_municipal_answers_images",
    )
    next_question_order = models.IntegerField(
        verbose_name="Порядок следующего вопроса", blank=True, null=True
    )
    order = models.IntegerField(
        verbose_name="Порядок",
        default=0,
    )
    type = models.CharField(
        verbose_name="Тип варианта ответа",
        max_length=50,
        choices=AnswerOptionType.CHOICES,
        default=AnswerOptionType.OPTION,
    )

    def __str__(self):
        return self.brief

    class Meta:
        verbose_name = "Вариант ответа на вопрос"
        verbose_name_plural = "Варианты ответа на вопрос"
