import collections

from django.contrib.gis.db import models as gis
from django.db import models
from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException


class LocalityTypeEnum(object):
    MUNICIPAL_REGION = 10
    MUNICIPAL_DISTRICT = 70
    URBAN_DISTRICT = 30

    SETTLEMENT = 20
    CITY = 40
    URBAN_VILLAGE = 50
    TOWNSHIP = 60

    MUNICIPALITY_TYPES = [MUNICIPAL_REGION, MUNICIPAL_DISTRICT, URBAN_DISTRICT]
    LOCALITY_TYPES = [SETTLEMENT, CITY, URBAN_VILLAGE, TOWNSHIP]

    RESOLVER = collections.OrderedDict(
        [
            (MUNICIPAL_REGION, "Муниципальный район"),
            (MUNICIPAL_DISTRICT, "Муниципальный округ"),
            (URBAN_DISTRICT, "Городской округ"),
            (SETTLEMENT, "Населенный пункт"),
            (CITY, "Город"),
            (URBAN_VILLAGE, "Поселок городского типа"),
            (TOWNSHIP, "Поселок"),
        ]
    )

    CHOICES = RESOLVER.items()


class LocalityCategory(object):
    MUNICIPALITY = 1
    LOCALITY = 2

    RESOLVER = collections.OrderedDict(
        [
            (MUNICIPALITY, "Муниципальное образование"),
            (LOCALITY, "Населённый пункт"),
        ]
    )

    CHOICES = RESOLVER.items()


def get_locality_type_short_name(locality_type):
    if locality_type is None:
        return ""

    if locality_type.name == "Муниципальный округ":
        return "окр"
    if locality_type.name == "Городской округ":
        return "г. р-н"
    if locality_type.name == "Город":
        return "г"
    if locality_type.name == "Поселок городского типа":
        return "пгт"
    if locality_type.name == "Поселок":
        return "п"
    return ""


class LocalityType(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование")
    category = models.IntegerField(choices=LocalityCategory.CHOICES, verbose_name="Категория")

    class Meta:
        verbose_name = 'Тип населённого пункта или муниципального образования'
        verbose_name_plural = 'Типы населённых пунктов и муниципальных образований'

    def __str__(self):
        return self.name


class LocalityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type__category=LocalityCategory.LOCALITY)


class MunicipalityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class DefaultLocalityManager(models.Manager):
    def get_localities(self):
        return self.get_queryset().filter(type__category=LocalityCategory.LOCALITY)

    def get_municipalities(self):
        return self.get_queryset().filter(type__category=LocalityCategory.MUNICIPALITY)


class Locality(models.Model):
    """
    Overengineered SETTLEMENT class
    """

    objects = DefaultLocalityManager()

    parent = models.ForeignKey(
        to="Municipality",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Муниципальное образование",
        related_name="localities",
    )
    name = models.TextField(
        verbose_name="Наименование",
    )
    type = models.ForeignKey(
        to=LocalityType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Тип населённого пункта или муниципального образования"
    )
    order = models.IntegerField(
        verbose_name="Порядок",
        default=0,
    )
    gis_center = gis.PointField(
        verbose_name="Центр",
        null=True,
        blank=True,
    )
    gis_border = gis.PolygonField(
        verbose_name="Граница",
        null=True,
        blank=True,
    )

    @property
    def type_short_name(self):
        return get_locality_type_short_name(self.type)

    @property
    def is_municipality(self):
        if not self.type:
            return False
        return self.type.category == LocalityCategory.MUNICIPALITY

    @property
    def is_locality(self):
        if not self.type:
            return False
        return self.type.category == LocalityCategory.MUNICIPALITY

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "Мунициипальное образование"
        verbose_name_plural = "Муниципальные образования"

        ordering = ["name"]

    def __str__(self):
        return self.name


class Municipality(Locality):

    objects = MunicipalityManager()

    def add_locality(self, locality):
        if not self.is_municipality:
            raise APIException(detail="invalid municipality")
        self.localities.add(locality)
        self.save()

    class Meta:
        verbose_name = "Муниципальное образование"
        verbose_name_plural = "Муниципальные образования"
        ordering = ["name"]
        proxy = True


class InhabitedLocality(Locality):
    """
    Логическая модель для населенного пункта
    """

    objects = LocalityManager()

    class Meta:
        verbose_name = "Населенный пункт"
        verbose_name_plural = "Населенные пункты"
        ordering = ["name"]
        proxy = True
