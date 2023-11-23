from modules.core.utils import CustomEnum


class VoteType(CustomEnum):
    """
    === Перечень: Тип голосования

    Доступные методы:

    * resolver()
    * choices()
    * max()
    * get(value)
    """

    REGIONAL = "Региональное"
    MUNICIPAL = "Муниципальное"
    LOCAL = "Локальное"
