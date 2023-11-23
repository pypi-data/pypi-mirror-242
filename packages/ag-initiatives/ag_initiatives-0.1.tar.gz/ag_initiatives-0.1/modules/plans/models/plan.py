from django.db import models

from modules.core.models import DepartmentStatus
from modules.subscriptions.mixins.subscribe_mixin import SubscribeMixin


class Plan(SubscribeMixin, models.Model):
    name = models.TextField(
        verbose_name="Наименование",
    )
    locality = models.ForeignKey(
        to="core.Locality",
        verbose_name="Муниципальное образование",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        to="plans.Category",
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )
    publication_date = models.DateTimeField(
        verbose_name="Дата размещения",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )
    location = models.OneToOneField(
        to="plans.Location",
        verbose_name="Местоположение",
        on_delete=models.SET_NULL,
        related_name="plan",
        blank=True, null=True,
    )
    files = models.ManyToManyField(
        to="plans.File",
        verbose_name="Файлы",
        blank=True,
    )
    owner = models.ForeignKey(
        to="core.Department",
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "План"
        verbose_name_plural = "Планы"
