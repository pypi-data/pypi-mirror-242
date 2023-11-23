import collections


class MainPageBlockType(object):
    INFORMATIONAL_MESSAGES = "INFORMATIONAL_MESSAGES"
    OFFICIALS = "OFFICIALS"
    STATS = "STATS"
    NEWS = "NEWS"
    VOTING = "VOTING"

    RESOLVER = collections.OrderedDict(
        [
            (INFORMATIONAL_MESSAGES, "Информационные сообщения"),
            (OFFICIALS, "Должностные лица"),
            (STATS, "Статистика"),
            (NEWS, "Новости"),
            (VOTING, "Голосования"),
        ]
    )

    CHOICES = RESOLVER.items()
