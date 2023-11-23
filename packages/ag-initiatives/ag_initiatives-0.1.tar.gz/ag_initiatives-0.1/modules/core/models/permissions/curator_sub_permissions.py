from django.db import models
from multiselectfield import MultiSelectField

from modules.core.models.permissions.modules_permissions import ModulesPermissions


class CuratorPermissions(models.Model):
    user_sub_permissions = models.ForeignKey(
        to='core.SubPermissions',
        on_delete=models.CASCADE,
        verbose_name='Дополнительные права пользователя',
        related_name='curator_permissions'
    )
    department = models.ForeignKey(
        to='core.Department',
        on_delete=models.CASCADE,
        verbose_name='Организация',
    )
    modules_permissions = MultiSelectField(
        choices=ModulesPermissions.CHOICES,
        verbose_name="Права модулей"
    )
    voting_categories = models.ManyToManyField(
        to='core.Category',
        verbose_name='Доступные категории голосований',
        blank=True,
        related_name='voting_categories',
    )
    voting_municipalities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='МО, по которым будут публиковаться голосования',
        blank=True,
        related_name='voting_municipalities',
    )
    voting_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='МО, по которым будут публиковаться голосования',
        blank=True,
        related_name='voting_localities',
    )
    initiatives_categories = models.ManyToManyField(
        to='initiatives.InitiativeCategory',
        verbose_name='Доступные категории инициатив',
        blank=True,
        related_name='initiatives_categories',
    )
    initiatives_municipalities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='МО, по которым будут рассматриваться инициативы',
        blank=True,
        related_name='initiatives_municipalities',
    )
    initiatives_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='МО, по которым будут рассматриваться инициативы',
        blank=True,
        related_name='initiatives_localities',
    )
    map_works_categories = models.ManyToManyField(
        to='map_works.WorkCategory',
        verbose_name='Доступные категории карт',
        blank=True,
        related_name='map_works_categories',
    )
    map_works_municipalities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования для карт',
        blank=True,
        related_name='map_works_municipalities',
    )
    map_works_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования для карт',
        blank=True,
        related_name='map_works_localities',
    )
    plans_categories = models.ManyToManyField(
        to='plans.Category',
        verbose_name='Доступные категории планов',
        blank=True,
        related_name='plans_categories',
    )
    plans_municipalities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования для планов',
        blank=True,
        related_name='plans_municipalities',
    )
    plans_localities = models.ManyToManyField(
        to='core.Locality',
        verbose_name='Доступные муниципальные образования для планов',
        blank=True,
        related_name='plans_localities',
    )
    is_active = models.BooleanField(
        default=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Дополнительные права пользователя для роли Куратор'
        verbose_name_plural = 'Дополнительные права пользователей для роли Куратор'

