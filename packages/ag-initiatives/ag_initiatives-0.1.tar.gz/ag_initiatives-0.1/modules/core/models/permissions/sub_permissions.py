import collections

from django.db import models

from modules.core.models import UserRole


class UserStatus:
    IS_ACTIVE = 'IS_ACTIVE'
    ARCHIVED = 'ARCHIVED'

    RESOLVER = collections.OrderedDict([
        (IS_ACTIVE, 'Активен'),
        (ARCHIVED, 'Архив')
    ])

    CHOICES = RESOLVER.items()


LKO_ROLES = [UserRole.ADMIN_LKO, UserRole.OPERATOR]


class SubPermissions(models.Model):
    user = models.OneToOneField(
        to='core.User',
        related_name='sub_permissions',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=255,
        choices=UserStatus.CHOICES,
        default=UserStatus.IS_ACTIVE,
        verbose_name="Статус"
    )
    position = models.CharField(
        max_length=255,
        verbose_name="Должность",
        null=True,
        blank=False
    )
    sub_phone = models.CharField(
        max_length=12,
        verbose_name="Добавочный номер телефона",
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Дополнительные права пользователя'
        verbose_name_plural = 'Дополнительные права пользователей'
