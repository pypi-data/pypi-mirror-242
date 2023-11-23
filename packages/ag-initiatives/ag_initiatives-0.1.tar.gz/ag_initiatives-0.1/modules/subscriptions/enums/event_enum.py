from collections import OrderedDict


class EventEnum(object):
    """Список событий"""

    @classmethod
    def __json__(cls):
        result = [
            OrderedDict({"name": key, "value": value}) for key, value in cls.CHOICES
        ]
        for index, event_data in enumerate(result):
            event = event_data["name"]
            if event in cls.VOTING:
                result[index]["module"] = "voting"
            elif event in cls.INITIATIVES:
                result[index]["module"] = "initiatives"
            elif event in cls.PLANS:
                result[index]["module"] = "plans"
            elif event in cls.MAP_WORKS:
                result[index]["module"] = "ap_works"
            elif event in cls.NEWS:
                result[index]["module"] = "core"
        return result

    NEW_VOTE_START = "NEW_VOTE_START"
    VOTE_END = "VOTE_END"
    INITIATIVE_NEW_VOTE_START = "INITIATIVE_NEW_VOTE_START"
    INITIATIVE_VOTE_END = "INITIATIVE_VOTE_END"
    DECISION_ON_INITIATIVE_PUBLICATION = "DECISION_ON_INITIATIVE_PUBLICATION"
    NEW_PLAN_PUBLICATION = "NEW_PLAN_PUBLICATION"
    REPAIR_WORK_PUBLICATION = "REPAIR_WORK_PUBLICATION"
    REPAIR_WORK_START = "REPAIR_WORK_START"
    REPAIR_WORK_END = "REPAIR_WORK_END"
    NEWS_PUBLICATION = "NEWS_PUBLICATION"

    RESOLVER = OrderedDict(
        {
            NEW_VOTE_START: "Начало нового голосования",
            VOTE_END: "Окончание голосования",
            INITIATIVE_NEW_VOTE_START: "Начало нового голосования по инициативе",
            INITIATIVE_VOTE_END: "Окончание голосования по инициативе",
            DECISION_ON_INITIATIVE_PUBLICATION: "Решение о публикации инициативы",
            NEW_PLAN_PUBLICATION: "Публикация нового плана",
            REPAIR_WORK_PUBLICATION: "Публикация ремонтных работ",
            REPAIR_WORK_START: "Начало ремонтных работ",
            REPAIR_WORK_END: "Окончание ремонтных работ",
            NEWS_PUBLICATION: "Публикация новостей",
        }
    )
    CHOICES = RESOLVER.items()
    VOTING = [NEW_VOTE_START, VOTE_END]
    INITIATIVES = [
        INITIATIVE_NEW_VOTE_START,
        INITIATIVE_VOTE_END,
        DECISION_ON_INITIATIVE_PUBLICATION,
    ]
    PLANS = [NEW_PLAN_PUBLICATION]
    MAP_WORKS = [
        REPAIR_WORK_PUBLICATION,
        REPAIR_WORK_START,
        REPAIR_WORK_END,
    ]
    NEWS = [NEWS_PUBLICATION]

    START_EVENT = [
        NEW_VOTE_START,
        INITIATIVE_NEW_VOTE_START,
        NEW_PLAN_PUBLICATION,
        REPAIR_WORK_START,
    ]

    PUBLISH_EVENT = [
        DECISION_ON_INITIATIVE_PUBLICATION,
        NEW_PLAN_PUBLICATION,
        REPAIR_WORK_PUBLICATION,
        NEWS_PUBLICATION,
    ]

    END_EVENT = [
        VOTE_END,
        INITIATIVE_VOTE_END,
        REPAIR_WORK_END,
    ]

    TYPE_RESOLVER = OrderedDict(
        {
            "START_EVENT": "Начало события",
            "PUBLISH_EVENT": "Публикация события",
            "END_EVENT": "Завершение события",
        }
    )
    TYPE_CHOICES = TYPE_RESOLVER.items()

    @classmethod
    def get(cls, value):
        return cls.RESOLVER.get(value, None)

    @classmethod
    def get_type(cls, value):
        return cls.TYPE_RESOLVER.get(value, None)
