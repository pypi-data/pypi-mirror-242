from django.db import models
from multiselectfield import MultiSelectField

from modules.core.models import UserRole


class MailInvite(models.Model):
    """Модель для заявок на создание пользователя"""
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=50,
    )
    patronymic_name = models.CharField(
        verbose_name="Отчество",
        null=True,
        blank=True,
        max_length=50,
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=127,
    )
    phone = models.TextField(
        verbose_name="Номер телефона",
        blank=True,
        null=True,
    )
    work_phone = models.CharField(
        verbose_name="Рабочий номер телефона",
        max_length=12,
        blank=True,
        null=True,
    )
    comment = models.TextField(
        verbose_name="Комментарий для электронного письма",
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        verbose_name="Название URL",
        unique=True,
        max_length=15,
    )
    sub_permission = models.ForeignKey(
        to="SubPermissions",
        verbose_name="Дополнительные права пользователя",
        on_delete=models.CASCADE,
    )
    admin_lko_permissions = models.ForeignKey(
        to='core.AdminLkoPermissions',
        on_delete=models.CASCADE,
        verbose_name='Права роли админ ЛКО',
        null=True,
        blank=True,
    )
    operator_permissions = models.ForeignKey(
        to='core.OperatorLkoPermissions',
        on_delete=models.CASCADE,
        verbose_name='Права роли оператора ЛКО',
        null=True,
        blank=True,
    )
    is_valid = models.BooleanField(
        default=True,
    )
    roles = MultiSelectField(
        choices=UserRole.CHOICES,
        verbose_name="Роли",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Заявка на заведение пользователя"
        verbose_name_plural = "Заявки на заведение пользователя"

    def __str__(self):
        return f"{self.slug}"


