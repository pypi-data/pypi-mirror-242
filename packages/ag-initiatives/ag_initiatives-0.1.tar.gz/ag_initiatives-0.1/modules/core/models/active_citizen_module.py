from collections import OrderedDict

from django.db import models, transaction


class ActiveCitizenModuleEnum(object):
    VOTING = 'voting'
    INITIATIVES = 'initiatives'
    APPEALS_POS = 'appeals_pos'
    ECOLOGY = 'ecology'
    ECOLOGY_STIMULATION = 'ecology_stimulation'
    ECOLOGY_OFFERS = 'ecology_offers'
    MAP_WORKS = 'map_works'
    PLANS = 'plans'
    FEEDBACK = 'feedback'
    NEWS = 'news'
    ABOUT_PROJECT = 'about_project'
    DIGITAL_CONSULTANT = 'digital_consultant'
    YOUR_OPINION = 'your_opinion'
    NEW_MODULE = 'new_module'

    RESOLVER = OrderedDict(
        [
            (VOTING, "Голосования"),
            (INITIATIVES, "Инициативы"),
            (APPEALS_POS, "Обращения граждан"),
            (ECOLOGY, "Бонусная программа"),
            (ECOLOGY_STIMULATION, "Бонусная программа. Поощрения"),
            (ECOLOGY_OFFERS, "Бонусная программа. Предложения"),
            (MAP_WORKS, "Карта ремонтных работ"),
            (PLANS, "Планы"),
            (FEEDBACK, "Обратная связь"),
            (NEWS, "Новости"),
            (ABOUT_PROJECT, "О проекте"),
            (DIGITAL_CONSULTANT, "Цифровой консультант"),
            (YOUR_OPINION, "Ваше мнение"),
            (NEW_MODULE, "Новый раздел"),
        ]
    )

    CHOICES = OrderedDict(list(zip(RESOLVER.keys(), RESOLVER.keys()))).items()
    DISPLAY_CHOICES = RESOLVER.items()


class ActiveCitizenModule(models.Model):
    """МОДЕЛЬ: МОДУЛЬ ПОРТАЛА"""

    name = models.CharField(
        verbose_name="Наименование",
        max_length=100,
        choices=ActiveCitizenModuleEnum.DISPLAY_CHOICES,
    )
    display_name = models.CharField(
        verbose_name="Отображаемое название",
        blank=True,
        max_length=255,
    )
    is_worked = models.BooleanField(verbose_name="В работе", default=True)

    def __str__(self):
        return f"{self.name} ({self.display_name})"

    def switch(self):
        self.is_worked = not self.is_worked
        self.save()

    class Meta:
        verbose_name = "Модуль портала"
        verbose_name_plural = "Модули портала"

        ordering = ("name",)
