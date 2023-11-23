import collections

from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition
from django.contrib.gis.db import models as gis


class AppealState(object):
    MODERATION = "MODERATION"
    MODERATION_ACCEPTED = "MODERATION_ACCEPTED"
    MODERATION_REJECTED = "MODERATION_REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    RESPONDED = "RESPONDED"

    RESOLVER = collections.OrderedDict(
        [
            (MODERATION, "Модерирование"),
            (MODERATION_REJECTED, "Отклонено"),
            (MODERATION_ACCEPTED, "На рассмотрении"),
            (IN_PROGRESS, "В работе"),
            (RESPONDED, "Получен ответ"),
        ]
    )

    CHOICES = RESOLVER.items()


class Appeal(models.Model):
    number = models.TextField(
        verbose_name="Регистрационный номер",
    )
    user = models.ForeignKey(
        to="core.User",
        verbose_name="Заявитель",
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
    )
    phone_number = models.TextField(
        verbose_name="Номер телефона",
    )
    creation_date_time = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    create_by_operator = models.BooleanField(
        verbose_name="Создано оператором",
        default=False,
    )
    category = models.ForeignKey(
        to="appeals.Category",
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )
    locality = models.ForeignKey(
        to="core.Locality",
        verbose_name="Муниципальное образование",
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        verbose_name="Описание проблемы",
    )
    files = models.ManyToManyField(
        to="File",
        verbose_name="Файлы",
        blank=True,
    )
    address = models.TextField(
        verbose_name="Адрес",
        blank=True,
    )
    gis_point = gis.PointField(
        verbose_name="Точка на карте",
    )
    is_public = models.BooleanField(
        verbose_name="Публичное",
        blank=True,
        null=True,
    )
    state = FSMField(
        choices=AppealState.CHOICES,
        verbose_name="Статус",
    )
    moderation_pass_date = models.DateTimeField(
        verbose_name="Дата завершения модерации",
        null=True,
        blank=True,
    )
    in_progress_begin_date = models.DateTimeField(
        verbose_name="Дата постановки в работу",
        null=True,
        blank=True,
    )
    responded_date = models.DateTimeField(
        verbose_name="Дата ответа на обращение",
        null=True,
        blank=True,
    )
    contractors = models.ManyToManyField(
        to="Contractor",
        verbose_name="Исполнители",
        blank=True,
    )

    @property
    def state_name(self):
        return AppealState.RESOLVER[self.state]

    @transition(
        field="state",
        source=[AppealState.MODERATION],
        target=AppealState.MODERATION_ACCEPTED,
    )
    def moderator_accept(self):
        self.moderation_pass_date = timezone.now()

    @transition(
        field="state",
        source=[AppealState.MODERATION],
        target=AppealState.MODERATION_REJECTED,
    )
    def moderator_reject(self):
        self.moderation_pass_date = timezone.now()

    @transition(
        field="state",
        source=[AppealState.MODERATION_ACCEPTED],
        target=AppealState.IN_PROGRESS,
    )
    def operator_in_progress(self):
        self.in_progress_begin_date = timezone.now()

    @transition(
        field="state", source=[AppealState.IN_PROGRESS], target=AppealState.RESPONDED
    )
    def operator_respond(self):
        self.responded_date = timezone.now()

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
