from enum import Enum


class SettingsTypes(Enum):
    """ Типы настроек. """
    INITIATIVE_PROPOSAL = "Инструкция по подаче инициативы"
    APPEAL_SUBMISSION = "Инструкция по подаче обращения"
    RULES_SUBMITTING_APPEAL = "Правила подачи обращения"
    BANNER = "Баннер на Главной странице"
    PERSONAL_DATA_USAGE_POLICY = "Политика использования персональных данных"
    OFFICIALS = "Должностные лица"
    USER_AGREEMENTS = "Соглашения пользователей"
