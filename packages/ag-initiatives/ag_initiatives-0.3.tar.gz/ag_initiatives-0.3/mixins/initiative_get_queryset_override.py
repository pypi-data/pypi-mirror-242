from django.db import models, ProgrammingError
from django.db import transaction
from django.utils import timezone
import factory
from django.db.models import signals


class QuerySetModified(models.query.QuerySet):
    pass


@factory.django.mute_signals(signals.pre_save, signals.post_save, signals.post_delete, signals.pre_delete)
def _end_votes_collection(initiative):
    if initiative.vote_finish_date and initiative.vote_finish_date >= timezone.now():
        return
    from modules.initiatives.models import UserInitiativeApprove
    votes_count = UserInitiativeApprove.objects.filter(
        initiative=initiative,
        timestamp__range=[
            initiative.votes_collection_begin_date,
            initiative.vote_finish_date,
        ],
    ).count()
    with transaction.atomic():
        if votes_count < initiative.votes_threshold:
            initiative.time_exceeded()
        else:
            initiative.necessary_votes_collected()
        initiative.save()


class NoDeleteManager(models.Manager):
    def get_queryset(self):
        try:
            from modules.initiatives.models import InitiativeState

            qs = QuerySetModified(self.model, using=self._db)
            for initiative in qs:
                if initiative.state == InitiativeState.VOTES_COLLECTION:
                    _end_votes_collection(initiative)
            return qs
        except ProgrammingError:
            return super().get_queryset()

class InitiativeGetQuerysetOverride(models.Model):
    """
    Переопределяет получение queryset у Initiative
    """

    objects = NoDeleteManager()

    class Meta:
        abstract = True
