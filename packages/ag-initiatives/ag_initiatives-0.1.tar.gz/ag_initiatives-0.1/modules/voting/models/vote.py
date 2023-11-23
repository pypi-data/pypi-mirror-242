import collections

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition

from modules.core.validators import FileSizeValidator
from modules.voting.enums import VoteType


class VoteState(object):
    DRAFT = "DRAFT"
    CREATED = "CREATED"

    MODERATION_ACCEPTED = "MODERATION_ACCEPTED"
    MODERATION_REJECTED = "MODERATION_REJECTED"

    OPERATOR_ACCEPTED = "OPERATOR_ACCEPTED"
    OPERATOR_REJECTED = "OPERATOR_REJECTED"

    PUBLISHED = "PUBLISHED"
    FINISHED = "FINISHED"

    RESOLVER = collections.OrderedDict(
        [
            (DRAFT, "Черновик"),
            (CREATED, "Модерирование"),
            (MODERATION_ACCEPTED, "Согласовано"),
            (MODERATION_REJECTED, "Отклонено модератором"),
            (OPERATOR_ACCEPTED, "Ожидает публикации"),
            (OPERATOR_REJECTED, "Отклонено оператором"),
            (PUBLISHED, "Открыто"),
            (FINISHED, "Завершено"),
        ]
    )

    CHOICES = RESOLVER.items()


class Vote(models.Model):
    """
    Конкретное голосование.
    Пример "Благоустройство дворов и территорий в 2020-2021 гг"
    """

    name = models.TextField(verbose_name="Название голосования")
    department = models.ForeignKey(
        "core.Department",
        on_delete=models.CASCADE,
        verbose_name="Инициатор голосования",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        "core.Category",
        on_delete=models.CASCADE,
        verbose_name="Тематические категории",
    )
    locality = models.ManyToManyField(
        to="core.Locality",
        verbose_name="Муниципальные образования",
    )
    type_publication_with_group_restriction = models.BooleanField(
        verbose_name="Категории участников голосования",
        default=False,
    )
    participants_groups = models.ManyToManyField(
        to="voting.LocalVotingGroup",
        verbose_name="Группы участников",
        blank=True,
    )
    participants_categories = models.ManyToManyField(
        to="core.CategoryCitizen",
        verbose_name="Категории участников",
        blank=True,
    )
    type_publication_with_age_restriction = models.BooleanField(
        verbose_name="Ограничение по возрасту участников голосования",
        default=False,
    )
    age_restriction_start = models.PositiveIntegerField(
        verbose_name="Минимальный возраст участников голосования",
        blank=True,
        null=True
    )
    age_restriction_finish = models.PositiveIntegerField(
        verbose_name="Максимальный возраст участников голосования",
        blank=True,
        null=True
    )
    multi_locality_vote = models.BooleanField(
        verbose_name="Разрешить голосовать в нескольких МО",
        default=True,
    )
    is_opened = models.BooleanField(default=False, verbose_name="Открыто")
    topic = models.TextField(
        blank=True,
        default="",
        verbose_name="Тема голосования",
    )
    description_vote = models.TextField(
        verbose_name="Описание голосования",
        blank=True,
        null=True
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    creation_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    start_date = models.DateTimeField(verbose_name="Дата начала голосования")
    end_date = models.DateTimeField(verbose_name="Дата завершения голосования")
    brief_image = models.ForeignKey(
        verbose_name="Изображение для карточки",
        help_text="(максимальный размер файла 5 МБ)",
        to="core.File",
        on_delete=models.CASCADE,
        related_name="votes_brief_images",
        null=True,
        blank=True,
    )
    image = models.ForeignKey(
        verbose_name="Изображение",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 5 МБ)",
        to="core.File",
        on_delete=models.CASCADE,
        related_name="votes_images",
    )
    video = models.ForeignKey(
        verbose_name="Видео",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 500 МБ)",
        to="core.Video",
        on_delete=models.CASCADE,
        related_name="votes_videos",
    )
    file = models.ForeignKey(
        verbose_name="Файл в формате .pdf",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 20 МБ)",
        to="core.File",
        on_delete=models.CASCADE,
        related_name="votes_files",
    )
    custom_url = models.TextField(
        verbose_name="Ссылка на внешний ресурс",
        default="",
        blank=True,
    )
    # todo: использовать поле state вместо is_opened и is_published
    state = FSMField(
        choices=VoteState.CHOICES,
        verbose_name="Статус",
    )
    to_moderation_date = models.DateTimeField(
        verbose_name="Дата направления на модерацию",
        null=True,
        blank=True,
    )
    moderation_date = models.DateTimeField(
        verbose_name="Дата модерациии",
        null=True,
        blank=True,
    )
    operator_action_date = models.DateTimeField(
        verbose_name="Дата реакции оператора после модерации",
        null=True,
        blank=True,
    )
    reject_reason_text = models.TextField(
        verbose_name="Причина отказа модератором",
        blank=True,
    )
    reject_reason_text_comment = models.TextField(
        verbose_name="Причина отказа модератором. Комментарий",
        blank=True,
    )
    operator_reject_reason_text = models.TextField(
        verbose_name="Причина отказа оператором",
        blank=True,
    )
    not_bonus_eligible = models.BooleanField(
        verbose_name="Не начислять бонусы", default=False
    )
    bonus_amount = models.PositiveIntegerField(
        verbose_name="Количество бонусов",
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        to="core.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def clean(self):
        if self.image:
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])(self.image.file)
            FileSizeValidator(5 * 1024 * 1024)(self.image.file)

        if self.video:
            FileSizeValidator(500 * 1024 * 1024)(self.video.file)

        if self.file:
            FileExtensionValidator(allowed_extensions=['pdf'])(self.file.file)
            FileSizeValidator(20 * 1024 * 1024)(self.file.file)

        if self.type_publication_with_age_restriction:
            if self.age_restriction_start is None or self.age_restriction_finish is None:
                raise ValidationError("Не заполнен минимальный или максимальный возраст участников голосования")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_start_date(self):
        return self.start_date.strftime("%d.%m.%Y")

    def get_end_date(self):
        return self.end_date.strftime("%d.%m.%Y")

    @transition(field="state", source=[VoteState.DRAFT], target=VoteState.CREATED)
    def operator_to_moderation(self):
        self.to_moderation_date = timezone.now()

    @transition(
        field="state", source=[VoteState.CREATED], target=VoteState.MODERATION_ACCEPTED
    )
    def moderator_accept(self):
        self.moderation_date = timezone.now()

    @transition(
        field="state", source=[VoteState.CREATED], target=VoteState.MODERATION_REJECTED
    )
    def moderator_reject(self):
        self.moderation_date = timezone.now()

    @transition(
        field="state",
        source=[VoteState.MODERATION_ACCEPTED],
        target=VoteState.OPERATOR_ACCEPTED,
    )
    def operator_accept(self):
        self.operator_action_date = timezone.now()

    @transition(
        field="state",
        source=[VoteState.MODERATION_ACCEPTED],
        target=VoteState.OPERATOR_REJECTED,
    )
    def operator_reject(self):
        self.operator_action_date = timezone.now()

    def __str__(self):
        return str(self.name) if self.name else "Голосование"

    class Meta:
        verbose_name = "Голосование"
        verbose_name_plural = "Голосования"
