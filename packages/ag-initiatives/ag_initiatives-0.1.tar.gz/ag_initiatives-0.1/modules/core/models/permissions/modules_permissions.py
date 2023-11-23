import collections


class ModulesPermissions:
    MAP_WORKS = "MAP_WORKS"
    PLANS = "PLANS"
    VOTING = "VOTING"
    INITIATIVES = "INITIATIVES"
    APPEALS = "APPEALS"
    ENCOURAGEMENTS = "ENCOURAGEMENTS"
    SUGGESTIONS = "SUGGESTIONS"

    RESOLVER = collections.OrderedDict([
        (MAP_WORKS, "Карты"),
        (PLANS, "Планы"),
        (VOTING, "Голосования"),
        (INITIATIVES, "Инициативы"),
        (APPEALS, "Ваше мнение"),
        (ENCOURAGEMENTS, "Система поощрений – Поощрения"),
        (SUGGESTIONS, "Система поощрений – Предложения")
    ])

    CHOICES = RESOLVER.items()
