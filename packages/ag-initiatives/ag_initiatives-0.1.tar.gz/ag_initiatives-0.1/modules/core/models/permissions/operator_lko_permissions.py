from django.db import models
from multiselectfield import MultiSelectField

from modules.core.models.permissions.modules_permissions import ModulesPermissions


class OperatorLkoPermissions(models.Model):
    user_sub_permissions = models.OneToOneField(
        to='core.SubPermissions',
        on_delete=models.SET_NULL,
        verbose_name='Дополнительные права пользователя',
        editable=False,
        related_name='operator_permissions',
        blank=True, null=True,
    )
    department = models.ForeignKey(
        to='core.Department',
        on_delete=models.CASCADE,
        verbose_name='Организация',
    )
    modules_permissions = MultiSelectField(
        choices=ModulesPermissions.CHOICES,
        verbose_name="Модуль"
    )
    voting_categories = models.ManyToManyField(
        to='core.Category',
        verbose_name='Категории для голосований',
        blank=True,
        related_name='operator_voting_categories_permissions',
    )
    voting_municipalities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='МО, по которым будут публиковаться голосования',
        blank=True,
        related_name='operator_voting_municipalies_permissions',
    )
    voting_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='МО, по которым будут публиковаться голосования',
        blank=True,
        related_name='operator_voting_categories_localities_permissions',
    )
    initiatives_categories = models.ManyToManyField(
        to='initiatives.InitiativeCategory',
        verbose_name='Категории для инициатив',
        blank=True,
        related_name='operator_initiatives_categories_permissions',
    )
    initiatives_municipalities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='МО, по которым будут рассматриваться инициативы',
        blank=True,
        related_name='operator_initiatives_municipalities_permissions',
    )
    initiatives_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='МО, по которым будут рассматриваться инициативы',
        blank=True,
        related_name='operator_initiatives_localities_permissions',
    )
    map_works_categories = models.ManyToManyField(
        to='map_works.WorkCategory',
        verbose_name='Категории для карт',
        blank=True,
        related_name='operator_map_works_categories_permissions',
    )
    map_works_municipalities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования для карт',
        blank=True,
        related_name='operator_map_works_municipalities_permissions',
    )
    map_works_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования для карт',
        blank=True,
        related_name='operator_map_works_localities_permissions',
    )
    plans_categories = models.ManyToManyField(
        to='plans.Category',
        verbose_name='Категории для планов',
        blank=True,
        related_name='operator_plans_categories_permissions',
    )
    plans_municipalities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования для планов',
        blank=True,
        related_name='operator_plans_municipalities_permissions',
    )
    plans_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования для планов',
        blank=True,
        related_name='operator_plans_localities_permissions',
    )
    appeals_categories = models.ManyToManyField(
        to='feedback.Problematic',
        verbose_name='Проблематика для модуля «Ваше мнение»',
        blank=True,
        related_name='operator_appeals_categories_permissions',
    )
    appeals_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования для модуля «Ваше мнение»',
        blank=True,
        related_name='operator_appeals_localities_permissions',
    )
    suggestion_categories = models.ManyToManyField(
        to='ecology.EventCategory',
        verbose_name='Тематические категории Предложений',
        blank=True,
        related_name='operator_suggestion_categories_permissions',
    )
    suggestion_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования Предложений',
        blank=True,
        related_name='operator_suggestion_localities_permissions',
    )
    encouragement_categories = models.ManyToManyField(
        to='ecology.GoodsNServicesItemCategory',
        verbose_name='Тематические категории Поощрений',
        blank=True,
        related_name='operator_encouragement_categories_permissions',
    )
    encouragement_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования Поощрений',
        blank=True,
        related_name='operator_encouragement_localities_permissions',
    )

    is_active = models.BooleanField(
        default=True,
        editable=False,
    )
    user = models.OneToOneField(
        to='core.User',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='operator_permissions'
    )
    # is_can_create_subdepartment = models.BooleanField(
    #     verbose_name="Доступность создания подведомственных организаций",
    #     default=False,
    # )
    # is_can_edit_department = models.BooleanField(
    #     verbose_name="Доступность редактирования Организации",
    #     default=False,
    # )
    # is_can_edit_subdepartment = models.BooleanField(
    #     verbose_name="Доступность редактирования Подведомственных организаций",
    #     default=False,
    # )
    def save(self, **kwargs):
        try:
            self.user = self.user_sub_permissions.user
        except Exception as e:
            print(e)
        return super().save(**kwargs)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Права доступа для роли Оператор'
        verbose_name_plural = 'Права доступа для роли Оператор'
