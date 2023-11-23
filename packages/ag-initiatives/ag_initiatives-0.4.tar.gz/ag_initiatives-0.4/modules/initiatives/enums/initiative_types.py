import collections


class InitiativeTypes(object):
    REGIONAL = "REGIONAL"
    MUNICIPAL = "MUNICIPAL"

    RESOLVER = collections.OrderedDict(
        [
            (REGIONAL, "Региональная"),
            (MUNICIPAL, "Муниципальная"),
        ]
    )

    CHOICES = RESOLVER.items()
