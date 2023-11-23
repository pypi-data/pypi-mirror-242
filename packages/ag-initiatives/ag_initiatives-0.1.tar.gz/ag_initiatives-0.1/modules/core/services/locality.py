from typing import Iterable, Set

from modules.core.models import Locality


class LocalityService:
    """
    Сервис, основное предназначение которого
    рекурсивно пробегаться по locality и возвращать всех его детей (и их детей)
    """

    @staticmethod
    def get_all_localities_generator(localities) -> Iterable[Locality]:
        """Рекурсивно достает всех детей, возвращает генератор"""

        if not hasattr(localities, "__iter__"):
            localities = [localities]
        for _locality in localities:
            yield _locality
            # sub_localities = _locality.localities.all()
            # if sub_localities:
            #     for _sub_locality in sub_localities:
            #         yield _sub_locality

    @classmethod
    def get_all_localities(cls, localities) -> Set[Locality]:
        """Получает всех уникальных детей переданных населенных пунктов или МО"""
        return set(cls.get_all_localities_generator(localities))

    @staticmethod
    def filter_localities(localities: Iterable[Locality]) -> Iterable[Locality]:
        """Получить только населенные пунткы из общего списка Locality"""
        return filter(lambda locality: locality.is_locality, localities)

    @staticmethod
    def filter_municipalities(localities: Iterable[Locality]) -> Iterable[Locality]:
        """Получить только МО из общего списка Locality"""
        return filter(lambda locality: locality.is_municipality, localities)
