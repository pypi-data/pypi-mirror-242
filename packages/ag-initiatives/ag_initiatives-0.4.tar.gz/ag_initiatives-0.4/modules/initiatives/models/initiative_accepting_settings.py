from django.db import models

from modules.core.models import DepartmentStatus
from modules.initiatives.enums import InitiativeSettingsTypes
from modules.initiatives.mixins import ModelWithDeletionProtection


class InitiativeAcceptingSettings(ModelWithDeletionProtection):
    # автоматически заполняется из данных пользователя
    department = models.ForeignKey(
        to="core.Department",
        verbose_name="Ведомство",
        on_delete=models.CASCADE,
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )
    type = models.CharField(
        max_length=20,
        choices=InitiativeSettingsTypes.CHOICES,
        default=InitiativeSettingsTypes.REGIONAL,
        verbose_name='Уровень реализации',
    )
    locality = models.ManyToManyField(
        to="core.Locality",
        blank=True,
        verbose_name="Муниципальные образования",
        related_name='initiative_settings',
    )
    category = models.ForeignKey(
        to="initiatives.InitiativeCategory",
        related_name="initiative_accepting_settings",
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )
    duration_month = models.PositiveIntegerField(
        verbose_name="Продолжительность голосования, месяцев"
    )
    votes_threshold = models.PositiveIntegerField(
        verbose_name="Пороговое значение количества голосов"
    )
    active = models.BooleanField(
        verbose_name="Активен",
    )

    @property
    def department_name(self):
        return self.department.name

    def __str__(self):
        return f'"{self.department}", {self.category}'

    class Meta:
        verbose_name = "Параметр приема инициативы"
        verbose_name_plural = "Параметры приема инициатив"
