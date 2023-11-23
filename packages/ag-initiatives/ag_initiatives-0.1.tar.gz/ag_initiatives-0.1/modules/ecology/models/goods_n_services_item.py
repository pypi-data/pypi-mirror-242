from dataclasses import dataclass

from django.db import models


@dataclass
class Coordinates:
    latitude: float
    longitude: float


class GoodsNServicesItem(models.Model):
    name = models.TextField(
        verbose_name="Наименование",
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )
    organization = models.ForeignKey(
        to="core.Department",
        verbose_name="Организация",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    category = models.ForeignKey(
        to="ecology.GoodsNServicesItemCategory",
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )
    locality = models.ForeignKey(
        to="core.Locality",
        on_delete=models.CASCADE,
        verbose_name="Муниципальное образование проведения",
    )

    display_localities = models.ManyToManyField(
        to="core.Locality",
        verbose_name="Муниципальные образования для отображения",
        related_name='display_localities_goods_n_services_item',
        blank=True,
    )
    cost = models.PositiveIntegerField(
        verbose_name="Цена за бонусы",
    )
    # TODO Объединение справочников 11.11.2023
    address = models.TextField(
        verbose_name="Адрес",
        null=True,
        blank=True,
    )

    coordinates = models.CharField(
        max_length=50,
        verbose_name="Координаты",
        null=True,
        blank=True,
    )

    multiple_purchase = models.BooleanField(
        verbose_name="Многократное приобретение поощрения пользователем",
        default=False,
    )

    maximum_purchasers = models.PositiveIntegerField(
        verbose_name="Ограничение на количество пользователей, которые могут получить поощрение",
        null=True,
        blank=True,
    )

    contacts = models.TextField(
        verbose_name="Описание контактных данных Партнера для получения Поощрения"
    )

    start_date = models.DateField(
        verbose_name="Дата начала",
        blank=True,
        null=True,
    )

    expiry_date = models.DateField(
        verbose_name="Дата окончания",
        blank=True,
        null=True,
    )

    start_time = models.TimeField(
        verbose_name="Время начала",
        blank=True,
        null=True,
    )

    expiry_time = models.TimeField(
        verbose_name="Время окончания",
        blank=True,
        null=True,
    )

    start_publication_date = models.DateField(
        verbose_name="Дата начала публикации", blank=True, null=True
    )

    expiry_publication_date = models.DateField(
        verbose_name="Дата конца публикации", blank=True, null=True
    )

    return_possibility = models.BooleanField(
        verbose_name="Возможность возврата", default=False
    )

    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=False,
    )

    def __str__(self):
        return self.name

    @property
    def object_coordinates(self):
        if not self.coordinates:
            return None
        coordinates = self.coordinates.split(",")
        return Coordinates(
            latitude=float(coordinates[0]), longitude=float(coordinates[1])
        )

    class Meta:
        verbose_name = "Поощрение"
        verbose_name_plural = "Поощрения"
