from collections import OrderedDict
from enum import Enum
from typing import Dict, Optional, ItemsView, Any


class CustomEnum(Enum):
    """
    === Базовый класс для перечней

    Доступные методы:

    * _resolver()_ - возвращает словарь
    +
    ----
    {ЗНАЧЕНИЕ: ОТОБРАЖАЕМОЕ ЗНАЧЕНИЕ}
    ----
    * _choices()_ - возвращает пары _dict_items_
    +
    ----
    (ЗНАЧЕНИЕ, ОТОБРАЖАЕМОЕ ЗНАЧЕНИЕ)
    ----
    * _max()_ - возвращает максимальный размер среди *ЗНАЧЕНИЙ*
    * _get(value)_ - возвращает *ОТОБРАЖАЕМОЕ ЗНАЧЕНИЕ* по ключу _value_
    """

    @classmethod
    def resolver(cls) -> Dict:
        result = OrderedDict({item.name: item.value for item in cls})
        return result

    @classmethod
    def choices(cls) -> ItemsView[str, str]:
        return cls.resolver().items()

    @classmethod
    def max(cls) -> int:
        return max([len(key) for key in cls.resolver().keys()])

    @classmethod
    def get(cls, value: str) -> Optional[str]:
        return cls.resolver().get(value)

    @classmethod
    def get_instance(cls, value: str) -> Optional[Any]:
        for item in cls:
            if value == item.name:
                return item

    def __str__(self):
        return self.value
