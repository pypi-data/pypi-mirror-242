import collections


class InitiativeType(object):
    """Enum для Тип Инициативы"""
    REGIONAL = "Региональные"
    MUNICIPAL = "Муниципальные"

    RESOLVER = collections.OrderedDict(
        [
            (REGIONAL, "Региональные инициативы"),
            (MUNICIPAL, "Муниципальные инициативы"),
        ]
    )

    CHOICES = RESOLVER.items()
