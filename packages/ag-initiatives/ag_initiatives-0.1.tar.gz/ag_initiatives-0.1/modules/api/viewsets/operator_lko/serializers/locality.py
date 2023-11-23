from typing import Iterable

from rest_framework import serializers
from rest_framework.utils import json

from modules.api.serializers import MunicipalityTreeSerializer, LocalityShortSerializer
from modules.core.models import Locality, Municipality, LocalityType
from modules.core.services.locality import LocalityService


class MunicipalityWithUnavailableTreeSerializer(MunicipalityTreeSerializer):
    localities = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    gis_center = serializers.SerializerMethodField(method_name="get_gis_center")

    class Meta:
        model = Locality
        fields = MunicipalityTreeSerializer.Meta.fields + [
            "is_available", "gis_center"
        ]

    def get_is_available(self, instance: Municipality):
        if hasattr(instance, "is_available"):
            return instance.is_available
        return True

    def get_localities(self, instance: Municipality):
        return None
        # if hasattr(instance, "allowed_localities"):
        #     return LocalityShortSerializer(instance.allowed_localities, many=True).data
        #
        # return LocalityShortSerializer(instance.localities.all(), many=True).data

    def get_gis_center(self, model: Locality):
        if model.gis_center is None:
            return None
        return json.loads(model.gis_center.geojson)


def get_municipalities_with_unavailable_from_localities(
        municipalities_with_localities: Iterable[Locality]
) -> Iterable[Locality]:
    """
    1. Фильтрует МО из общего списка МО и населенных пунктов
    2. Фильтрует населенные пункты, которые не являются детьми этих МО
    3. Достает MO из населенных пунктов во 2 пункте, метит их как недоступные, присваивает ему только доступных детей
        (они будут недоступны для редактирования, создания каких либо объектов)
    4. Объединяет их вместе

    Далее это все должно улетать в сериализатор, который знает о метках доступных, недоступных МО,
        а не просто строит дерево из всех существующих детей
    """
    locality_service = LocalityService()
    municipalities = list(locality_service.filter_municipalities(municipalities_with_localities))

    localities = locality_service.filter_localities(municipalities_with_localities)

    localities_from_municipalities = list(locality_service.filter_localities(
        locality_service.get_all_localities(municipalities)
    ))
    localities_without_municipalities = list(
        filter(lambda locality: locality not in localities_from_municipalities, localities)
    )

    unavailable_municipalities = []
    for locality in localities_without_municipalities:
        municipality = locality.parent

        if municipality is not None:

            if not hasattr(municipality, "is_available"):
                municipality.is_available = False

            if municipality not in unavailable_municipalities:
                unavailable_municipalities.append(municipality)

            for local_municipality in unavailable_municipalities:
                if municipality == local_municipality:
                    if not hasattr(local_municipality, "allowed_localities"):
                        local_municipality.allowed_localities = []

                    local_municipality.allowed_localities.append(locality)
                    break

    return municipalities + unavailable_municipalities
