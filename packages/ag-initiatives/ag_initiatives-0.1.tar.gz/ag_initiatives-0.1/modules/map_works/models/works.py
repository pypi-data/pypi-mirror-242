import collections

from django.db import models
from django.utils import timezone

from modules.core.models import DepartmentStatus
from modules.subscriptions.mixins.subscribe_mixin import SubscribeMixin


class WorksState(object):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

    RESOLVER = collections.OrderedDict(
        [
            (PLANNED, "Запланировано"),
            (IN_PROGRESS, "В работе"),
            (COMPLETED, "Завершено"),
        ]
    )

    CHOICES = RESOLVER.items()


class Works(SubscribeMixin, models.Model):
    locality = models.ForeignKey(
        to="core.Locality",
        verbose_name="Муниципальное образование",
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        to="map_works.WorkCategory",
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )

    reason = models.ForeignKey(
        to="map_works.WorkReason",
        verbose_name="Причина",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    begin_datetime = models.DateTimeField(
        verbose_name="Дата-время начала работ",
    )

    end_datetime = models.DateTimeField(
        verbose_name="Дата-время окончания работ",
    )

    private_territory = models.BooleanField(
        verbose_name="Частный сектор",
        null=True,
        blank=True,
    )

    institution_type = models.ForeignKey(
        to="map_works.InstitutionType",
        verbose_name="Тип учреждения",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    work_type = models.ForeignKey(
        to="map_works.WorkType",
        verbose_name="Тип работ",
        on_delete=models.CASCADE,
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )

    objects_description = models.TextField(
        verbose_name="Описание объектов",
        blank=True,
    )

    contractor = models.ForeignKey(
        to="map_works.Contractor",
        verbose_name="Подрядчик",
        on_delete=models.CASCADE,
    )

    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
    )

    owner = models.ForeignKey(
        to="core.Department",
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )

    class Meta:
        verbose_name = "Работы"
        verbose_name_plural = "Работы"

    @property
    def state(self):
        now_time = timezone.now()

        if now_time < self.begin_datetime:
            return WorksState.PLANNED
        elif self.begin_datetime < now_time < self.end_datetime:
            return WorksState.IN_PROGRESS
        elif now_time > self.end_datetime:
            return WorksState.COMPLETED

        return None

    @property
    def state_label(self):
        return WorksState.RESOLVER[self.state]
