from django.contrib.gis.db import models as gis
from django.db import models


class Location(models.Model):
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
