import collections


class VotingType(object):
    """Enum Тип Голосования"""

    REGIONAL = "Региональные"
    MUNICIPAL = "Муниципальные"
    LOCAL = "Локальные"

    RESOLVER = collections.OrderedDict(
        [
            (REGIONAL, "Региональные голосования"),
            (MUNICIPAL, "Муниципальные голосования"),
            (LOCAL, "Локальные голосования"),
        ]
    )

    CHOICES = RESOLVER.items()
