from typing import Dict, Union, List

from modules.core.enum import ReportTypeEnum


class ReportTypeFilter(object):
    """
    ==== Фильтр типов отчётов

    Фильтрует перечисление ReportTypeEnum для API

    Фильтрация осуществляется:

    * по типу:
    ** administrator_lko_reports - отчёты администратора ЛКО;
    ** operator_lko_reports - отчёты оператора ЛКО;
    ** regional_reports - региональные отчёты;
    ** local_reports - локальные отчёты;
    ** municipal_reports - муниципальные отчёты;
    * по названию отчёта.

    Допустимы множественные значения.

    """

    class Meta:
        enum = ReportTypeEnum

    _meta = Meta()
    data: Dict = _meta.enum.resolver()

    def __init__(self, **kwargs) -> None:
        """Инициализация класса с входящим словарём из GET-запроса"""
        self.submit_filter(kwargs)

    def submit_filter(self, filter_values: Dict):
        """Применение фильтров"""
        for key, value in filter_values.items():
            if key == "type":
                self.filter_by_type(self._clear_value(value))
            elif key == "name":
                self.filter_by_name(self._clear_value(value))
        return self

    def __call__(self, *args, **kwargs) -> "ReportTypeFilter":
        """Вызов класса"""
        return self

    @classmethod
    def _clear_value(cls, value: Union[str, List]) -> List:
        """Очистка значений фильтров - форматирование в список"""
        if isinstance(value, str):
            return value.split(",")
        return value

    def filter_by_type(self, value: List) -> "ReportTypeFilter":
        """Фильтрация по типу (категории)"""
        data = {}
        for item in value:
            if item in [
                "administrator_lko_reports",
                "operator_lko_reports",
                "regional_reports",
                "local_reports",
                "municipal_reports",
            ]:
                data.update(eval(f"self._meta.enum.{item}()"))
            self.data = data.copy()
        return self

    def filter_by_name(self, value: List) -> "ReportTypeFilter":
        """Фильтрация по названию"""
        data = {}
        for item in value:
            if item in list(self._meta.enum.resolver().keys()):
                data.update({item: self._meta.enum.get(item)})
            self.data = data.copy()
        return self
