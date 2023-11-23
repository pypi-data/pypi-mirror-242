from typing import Dict

from modules.core.utils import CustomEnum


class ReportTypeEnum(CustomEnum):
    USER_LIST_REPORT = "Отчёт по пользователям"

    SUMMARY_REGIONAL_REPORT = "Сводный отчёт по всем муниципальным округам"
    DETAILED_REGIONAL_REPORT = "Развёрнутый отчёт по всем муниципальным округам"
    USER_RESPONSES_REGIONAL_REPORT = (
        "Отчёт по ответам пользователей по всем муниципальным округам"
    )
    SUMMARY_REGIONAL_REPORT_WITH_MUNICIPAL_DISTRICT_DETAIL = (
        "Сводные отчёты по каждому муниципальному округу"
    )
    DETAILED_REGIONAL_REPORT_WITH_MUNICIPAL_DISTRICT_DETAIL = (
        "Развёрнутые отчёты по каждому муниципальному округу"
    )

    SUMMARY_MUNICIPAL_REPORT_WITH_MUNICIPAL_DISTRICT_DETAIL = (
        "Сводные отчёты по каждому муниципальному округу (населённому пункту)"
    )
    USER_RESPONSES_MUNICIPAL_REPORT = "Отчёт по ответам пользователей по всем муниципальным округам (населённым пунктам)"
    DETAILED_MUNICIPAL_REPORT_WITH_MUNICIPAL_DISTRICT_DETAIL = (
        "Развёрнутые отчёты по каждому муниципальному округу (населённому пункту)"
    )

    SUMMARY_LOCAL_REPORT = "Сводный отчёт по всем группам участников"
    DETAILED_LOCAL_REPORT = "Развёрнутый отчёт по всем группам участников"
    USER_RESPONSES_LOCAL_REPORT = (
        "Отчёт по ответам пользователей по всем группам участников"
    )
    SUMMARY_LOCAL_REPORT_WITH_GROUP_DETAIL = "Сводный отчёт по каждой группе участников"
    DETAILED_LOCAL_REPORT_WITH_GROUP_DETAIL = (
        "Развёрнутый отчёт по каждой группе участников"
    )

    @classmethod
    def administrator_lko_reports(cls) -> Dict:
        """Перечень отчётов администратора ЛКО"""
        return {cls.USER_LIST_REPORT.name: cls.USER_LIST_REPORT.value}

    @classmethod
    def operator_lko_reports(cls):
        """Перечень отчётов оператора ЛКО"""
        return {
            key: value
            for key, value in cls.resolver().items()
            if key not in cls.administrator_lko_reports()
        }

    @classmethod
    def regional_reports(cls):
        """Перечень региональных отчётов"""
        return {
            key: value for key, value in cls.resolver().items() if "REGIONAL" in key
        }

    @classmethod
    def local_reports(cls):
        """Перечень локальных отчётов"""
        return {key: value for key, value in cls.resolver().items() if "LOCAL" in key}

    @classmethod
    def municipal_reports(cls):
        """Перечень муниципальных отчётов"""
        return {
            key: value
            for key, value in cls.resolver().items()
            if "MUNICIPAL" in key
            and key not in cls.regional_reports()
            and key not in cls.local_reports()
        }
