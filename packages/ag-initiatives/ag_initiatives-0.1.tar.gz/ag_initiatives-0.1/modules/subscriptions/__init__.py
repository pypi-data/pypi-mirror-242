"""
Модуль subscriptions (Подписки пользователей)

Данный модуль предоставляет функционал
для оформления подписки по следующим событиям:

* _NEW_VOTE_START_ - Начало нового голосования
* _VOTE_END_ - Окончание голосования
* _INITIATIVE_NEW_VOTE_START_ - Начало нового голосования по инициативе
* _INITIATIVE_VOTE_END_ - Окончание голосования по инициативе
* _DECISION_ON_INITIATIVE_PUBLICATION_ - Решение о публикации инициативы
* _NEW_PLAN_PUBLICATION_ - Публикация нового плана
* _REPAIR_WORK_PUBLICATION_ - Публикация ремонтных работ
* _REPAIR_WORK_START_ - Начало ремонтных работ
* _REPAIR_WORK_END_ - Окончание ремонтных работ
* _NEWS_PUBLICATION_ - Публикация новостей"""


default_app_config = "modules.subscriptions.apps.SubscriptionsConfig"
__version__ = 1.0
__author__ = "Кирилл Стрелковский"
