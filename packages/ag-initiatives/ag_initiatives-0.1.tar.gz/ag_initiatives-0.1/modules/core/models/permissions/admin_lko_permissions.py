from django.db import models


class AdminLkoPermissions(models.Model):
    sub_permissions = models.OneToOneField(
        'core.SubPermissions',
        on_delete=models.SET_NULL,
        verbose_name='Дополнительные права роли админ ЛКО',
        editable=False,
        related_name='admin_lko_permissions',
        blank=True, null=True,
    )
    department = models.ForeignKey(
        to='core.Department',
        on_delete=models.CASCADE,
        verbose_name='Организация'
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
        related_name='admin_lko_permissions',
    )
    is_can_create_subdepartment = models.BooleanField(
        verbose_name="Доступность создания подведомственных организаций",
        default=False,
    )
    is_can_edit_department = models.BooleanField(
        verbose_name="Доступность редактирования Организации",
        default=False,
    )
    is_can_edit_subdepartment = models.BooleanField(
        verbose_name="Доступность редактирования Подведомственных организаций",
        default=False,
    )

    def save(self, **kwargs):
        try:
            self.user = self.sub_permissions.user
        except Exception as e:
            print(e)
        return super().save(**kwargs)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Права доступа для роли Администратор ЛКО"
        verbose_name_plural = "Права доступа для роли Администратор ЛКО"
