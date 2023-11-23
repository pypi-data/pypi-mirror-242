from django.db import models
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField

from modules.core.models import DepartmentStatus
from modules.core.models.permissions import ModulesPermissions


class DepartmentSubPermissions(models.Model):

    department = models.OneToOneField(
        to="core.Department",
        on_delete=models.CASCADE,
        verbose_name="Организация",
        related_name="sub_permissions",
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )
    modules_permissions = MultiSelectField(
        choices=ModulesPermissions.CHOICES,
        verbose_name="Настройки доступа к модулям ПО"
    )
    voting_categories = models.ManyToManyField(
        to="core.Category",
        verbose_name="Категории для голосований",
        related_name="department_voting_categories_permissions",
        blank=True
    )
    initiative_categories = models.ManyToManyField(
        to="initiatives.InitiativeCategory",
        verbose_name="Категории для инициатив",
        related_name="department_initiatives_categories_permissions",
        blank=True
    )
    map_works_categories = models.ManyToManyField(
        to='map_works.WorkCategory',
        verbose_name='Категории для карт',
        blank=True,
        related_name='department_map_works_categories_permissions',
    )
    plans_categories = models.ManyToManyField(
        to='plans.Category',
        verbose_name='Категории для планов',
        blank=True,
        related_name='department_plans_categories_permissions',
    )
    appeals_categories = models.ManyToManyField(
        to='feedback.Problematic',
        verbose_name='Проблематика для модуля «Ваше мнение»',
        blank=True,
        related_name='department_appeals_categories_permissions',
    )
    suggestion_categories = models.ManyToManyField(
        to='ecology.EventCategory',
        verbose_name='Тематические категории для "Системы поощрения – Предложения"',
        blank=True,
        related_name='department_ecology_suggestion_categories_permissions',
    )
    encouragement_categories = models.ManyToManyField(
        to='ecology.GoodsNServicesItemCategory',
        verbose_name='Тематические категории для "Системы поощрения – Поощрения"',
        blank=True,
        related_name='department_ecology_encouragement_categories_permission',
    )

    def __str__(self):
        return str(self.department)

    def clean(self):
        valid_permissions = [
            ModulesPermissions.MAP_WORKS,
            ModulesPermissions.PLANS,
            ModulesPermissions.VOTING,
            ModulesPermissions.INITIATIVES,
            ModulesPermissions.APPEALS,
            ModulesPermissions.ENCOURAGEMENTS,
            ModulesPermissions.SUGGESTIONS
        ]

        if not any(permission in valid_permissions for permission in self.modules_permissions):
            raise ValidationError("Должно быть заполнено хотя бы одно поле из прав модулей.")

    class Meta:
        verbose_name = "Дополнительные права для организации"
        verbose_name_plural = "Дополнительные права для организаций"
