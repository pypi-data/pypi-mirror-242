import collections


class InitiativeState(object):
    PREMODERATION = "PREMODERATION"  # Модерирование модератором
    PREMODERATION_REJECTED = "PREMODERATION_REJECTED"  # Модерирование модератором
    CHANGES_APPROVAL = "CHANGES_APPROVAL"
    MODERATION = "MODERATION"  # Модерирование оператором
    REJECTED = "REJECTED"
    CREATED = "CREATED"
    VOTES_COLLECTION = "VOTES_COLLECTION"
    REJECTED_VOTES_THRESHOLD = "REJECTED_VOTES_THRESHOLD"
    CONSIDERATION = "CONSIDERATION"
    IN_PROGRESS = "IN_PROGRESS"
    ACCOMPLISHED = "ACCOMPLISHED"

    RESOLVER = collections.OrderedDict(
        [
            (PREMODERATION, "Модерирование"),
            (PREMODERATION_REJECTED, "Отклонена по итогам модерации"),
            (CHANGES_APPROVAL, "Согласование изменений"),
            (MODERATION, "Экспертная оценка"),
            (REJECTED, "Отклонена"),
            (VOTES_COLLECTION, "Сбор голосов"),
            (REJECTED_VOTES_THRESHOLD, "Порог голосования не пройден"),
            (CONSIDERATION, "На рассмотрении"),
            (IN_PROGRESS, "Принято решение"),
            (ACCOMPLISHED, "Реализовано"),
        ]
    )

    CHOICES = RESOLVER.items()
