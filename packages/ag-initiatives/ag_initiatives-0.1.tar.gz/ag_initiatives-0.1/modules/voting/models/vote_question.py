from django.core.validators import FileExtensionValidator
from django.db import models

from modules.core.validators import FileSizeValidator


class VoteQuestion(models.Model):
    """
    Вопрос голосования.
    Пример "Какой двор Вы бы хотели видеть благоустроенным к 2021 году?"
    """

    vote = models.ForeignKey(
        to="voting.Vote",
        verbose_name="Голосование",
        related_name="questions",
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
        related_name="vote_questions_images",
    )
    video = models.ForeignKey(
        verbose_name="Видео",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 500 МБ)",
        to="core.Video",
        on_delete=models.CASCADE,
        related_name="vote_questions_videos",
    )
    file = models.ForeignKey(
        verbose_name="Файл в формате .pdf",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 20 МБ)",
        to="core.File",
        on_delete=models.CASCADE,
        related_name="vote_questions_files",
    )
    is_custom_answer_allowed = models.BooleanField(  # temporary unused
        default=False,
        verbose_name="Возможен вариант пользователя",
        blank=True,
    )
    custom_answer_length = models.PositiveIntegerField(
        verbose_name="Ограничение на количество символов свободного ответа",
        blank=True,
        null=True,
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
    use_question_branches = models.BooleanField(
        verbose_name="Ветвление", default=False
    )

    def __str__(self):
        return self.brief if len(self.brief) else "Вопрос"

    def clean(self):
        if self.photo:
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])(self.photo.file)
            FileSizeValidator(5 * 1024 * 1024)(self.photo.file)

        if self.video:
            FileSizeValidator(500 * 1024 * 1024)(self.video.file)

        if self.file:
            FileExtensionValidator(allowed_extensions=['pdf'])(self.file.file)
            FileSizeValidator(20 * 1024 * 1024)(self.file.file)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Вопрос голосования"
        verbose_name_plural = "Вопросы голосования"
