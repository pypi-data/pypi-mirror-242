from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition

from .vote import VoteState


class VoteLocal(models.Model):
    """
    Конкретное локальное голосование.
    Пример "Благоустройство дворов и территорий в 2020-2021 гг"
    """

    name = models.TextField(verbose_name="Название голосования")
    department = models.ForeignKey(
        "core.Department",
        on_delete=models.CASCADE,
        verbose_name="Инициатор голосования",
        blank=True,
    )
    municipal_formation = models.ManyToManyField(
        to="core.Municipality",
        verbose_name="Муниципальное образование",
        related_name = "vote_municipality_local",
    )
    locality = models.ManyToManyField(
        to="core.Locality",
        verbose_name="Населенный пункт",
        blank=True,
        related_name = "vote_locality_local"
    )
    category = models.ForeignKey(
        "core.Category",
        on_delete=models.CASCADE,
        verbose_name="Тематическая категория",
    )
    brief_image = models.ForeignKey(
        verbose_name="Изображение для карточки голосования",
        help_text="(максимальный размер файла 5 МБ)",
        to="core.File",
        on_delete=models.CASCADE,
        related_name="votes_local_brief_images",
    )
    start_date = models.DateField(verbose_name="Дата начала голосования")
    end_date = models.DateField(verbose_name="Дата завершения голосования")
    participants_groups = models.ManyToManyField(
        to="voting.LocalVotingGroup",
        verbose_name="Группы участников",
        blank=True,
        related_name="groups",
    )
    description_vote = models.TextField(verbose_name="Описание голосования", blank=True)
    access_interim_results = models.BooleanField(
        verbose_name="Доступ к просмотру промежуточных результатов голосования",
        default=False,
        blank=True,
    )
    access_total_results = models.BooleanField(
        verbose_name="Доступ к просмотру промежуточных результатов голосования",
        default=False,
        blank=True,
    )
    is_opened = models.BooleanField(default=False, verbose_name="Открыто")
    topic = models.TextField(
        blank=True,
        default="",
        verbose_name="Тема голосования",
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    creation_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
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
    use_question_branches = models.BooleanField(
        verbose_name="Использовать механизм ветвления вопросов", default=False
    )
    image = models.ForeignKey(
        verbose_name="Изображение",
        null=True,
        blank=True,
        help_text="(максимальный размер файла 5 МБ)",
        to="core.File",
        on_delete=models.CASCADE,
        related_name="local_vote_image",
    )
    moderate = models.BooleanField(default=True, verbose_name="Нужна модерация?")

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
        return self.name if len(self.name) else "Голосование"

    class Meta:
        verbose_name = "Локальное голосование"
        verbose_name_plural = "Локальные голосования"