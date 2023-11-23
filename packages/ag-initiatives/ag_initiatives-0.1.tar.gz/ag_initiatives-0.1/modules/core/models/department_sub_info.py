import collections

from django.db import models

from modules.core.models import DepartmentStatus


class LkoLevel(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Уровень ЛКО'
        verbose_name_plural = 'Уровни ЛКО'

    def __str__(self):
        return self.name


class LkoType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Тип ЛКО'
        verbose_name_plural = 'Типы ЛКО'

    def __str__(self):
        return self.name


class DepartmentSubInfo(models.Model):
    department = models.OneToOneField(
        to="core.Department",
        on_delete=models.CASCADE,
        verbose_name="Организация",
        related_name="sub_info",
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )
    short_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Краткое название"
    )
    address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Адрес"
    )
    ogrn = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="ОГРН"
    )
    inn = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="ИНН"
    )
    kpp = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="КПП"
    )
    oktmo = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="ОКТМО"
    )
    lko_level = models.ForeignKey(
        LkoLevel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Уровень ЛКО"
    )
    lko_type = models.ForeignKey(
        LkoType,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Тип ЛКО"
    )

    class Meta:
        verbose_name = "Дополнительная информация об организации"
        verbose_name_plural = "Дополнительная информация об организациях"
