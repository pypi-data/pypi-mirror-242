from dataclasses import dataclass

from django.db import models


@dataclass
class Coordinates:
    latitude: float
    longitude: float


class Event(models.Model):
    name = models.TextField(
        verbose_name="Наименование",
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    ) 
    # TODO Объединение справочников 11.11.2023
    organization = models.ForeignKey(
        to="core.Department",
        verbose_name="Организация",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    category = models.ForeignKey(
        to="ecology.EventCategory",
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
        related_name='display_localities_event',
        blank=True,
    )

    reward = models.PositiveIntegerField(
        verbose_name="Количество начисляемых бонусов за участие",
    )

    multiple_participation = models.BooleanField(
        verbose_name="Многократное участие",
        default=False,
    )

    maximum_participants = models.PositiveIntegerField(
        verbose_name="Максимальное количество участников",
        null=True,
        blank=True,
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
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"
