from django.db import models
from django.db.models import Case, When, Value, QuerySet

from modules.initiatives.models import InitiativeState


class Annotator:
    @classmethod
    def annotate_for_sorting(cls, query: QuerySet, is_additional: bool = False):
        return query.annotate(
            sort_field=Case(
                When(state=InitiativeState.MODERATION, then=Value(1)),
                When(state=InitiativeState.REJECTED, then=Value(30)),
                When(state=InitiativeState.REJECTED_VOTES_THRESHOLD, then=Value(50)),
                default=Value(20),
                output_field=models.IntegerField(),
            ),
            is_additional=Value(
                value=is_additional, output_field=models.BooleanField()
            ),
        )

    @classmethod
    def union(cls, base_query: QuerySet, additional_query: QuerySet):
        return cls.annotate_for_sorting(base_query, False).union(
            cls.annotate_for_sorting(additional_query, True)
        )
