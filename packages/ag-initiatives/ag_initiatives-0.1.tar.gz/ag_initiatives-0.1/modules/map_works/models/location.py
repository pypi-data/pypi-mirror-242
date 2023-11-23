from django.contrib.gis.db import models as gis
from django.db import models


class Location(models.Model):
    work = models.ForeignKey(
        to="map_works.Works",
        verbose_name="Работы",
        on_delete=models.CASCADE,
        related_name="locations",
    )

    address = models.TextField(
        verbose_name="Адрес",
        blank=True,
    )

    gis_point = gis.PointField(
        verbose_name="Центр",
        null=True,
        blank=True,
    )

    gis_polygon = gis.PolygonField(
        verbose_name="Граница",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"
