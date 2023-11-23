from django.db import models


class VoteRegionalQuestion(models.Model):
    """
    Вопрос голосования.
    Пример "Какой двор Вы бы хотели видеть благоустроенным к 2021 году?"
    """

    vote = models.ForeignKey(
        to="voting.VoteRegional",
        verbose_name="Голосование",
        related_name="regional_questions",
        on_delete=models.CASCADE,
    )
    brief = models.TextField(default="", verbose_name="Краткое описание вопроса")
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Полное описание вопроса",
    )
    photo = models.ForeignKey(
        null=True,
        blank=True,
        verbose_name="Вспомогательное изображение",
        help_text="(максимальный размер файла 5 МБ)",
        to="core.File",
        on_delete=models.CASCADE,
        related_name="vote_regional_questions_images",
    )
    is_custom_answer_allowed = models.BooleanField(  # temporary unused
        default=False,
        verbose_name="Возможен вариант пользователя",
        blank=True,
    )
    is_multi_answer_allowed = models.BooleanField(
        default=False,
        verbose_name="Несколько ответов",
        blank=True,
    )
    max_answer_option_count = models.PositiveIntegerField(
        default=1,
        verbose_name="Максимальное количество вариантов ответов доступных пользователю",
    )
    order = models.IntegerField(
        verbose_name="Порядок",
        default=0,
    )
    always_visible = models.BooleanField(
        verbose_name="Показывать независимо от ссылок", default=False
    )

    def __str__(self):
        return self.brief if len(self.brief) else "Вопрос"

    class Meta:
        verbose_name = "Вопросы для регионального голосования"
        verbose_name_plural = "Вопросы для региональных голосований"
