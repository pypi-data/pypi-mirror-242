import collections

from django.db import models


class DepartmentStatus:
    IS_ACTIVE = 'IS_ACTIVE'
    ARCHIVED = 'ARCHIVED'

    RESOLVER = collections.OrderedDict([
        (IS_ACTIVE, 'Активно'),
        (ARCHIVED, 'В архиве')
    ])

    CHOICES = RESOLVER.items()


class Department(models.Model):
    """
    Министерство/Направление дейстельности/Глобальная тема.
    У министерства может быть несколько категорий голосования.
    Пример "Министерство Строительства и городского хозяйства"
    """

    parent = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
        related_name="sub_departments",
        verbose_name="Вышестоящая организация",
    )
    name = models.TextField(unique=True, verbose_name="Полное название")
    email = models.TextField(
        verbose_name="Адрес электронной почты",
    )
    locality = models.ManyToManyField(
        to="core.Locality",
        verbose_name="МО",
        related_name='departments',
    )
    # todo переименовать в email_notification
    email_initiative_notification = models.BooleanField(
        verbose_name="Уведомления по почте",
        default=True,
    )
    image = models.ImageField(
        verbose_name="Иконка", help_text="(максимальный размер файла 5 МБ)"
    )
    additional_filtering = models.BooleanField(
        default=False,
        verbose_name="Отображать инициативы по выбранным муниципальным образованиям и категориям.",
    )
    categories = models.ManyToManyField(
        to="initiatives.InitiativeCategory",
        blank=True,
        verbose_name="Категории для отображения",
    )
    status = models.CharField(
        max_length=255,
        choices=DepartmentStatus.CHOICES,
        default=DepartmentStatus.IS_ACTIVE,
        verbose_name='Статус'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

        ordering = ["name"]
