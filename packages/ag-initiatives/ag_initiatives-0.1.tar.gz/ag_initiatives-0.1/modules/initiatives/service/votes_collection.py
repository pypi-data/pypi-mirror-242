from time import timezone

from django.db import transaction
from django.utils import timezone

from modules.initiatives import models as initiatives


def _end_votes_collection(pk: int):
    initiative = initiatives.Initiative.objects.get(pk=pk)
    if initiative.vote_finish_date >= timezone.now():
        return
    votes_count = initiatives.UserInitiativeApprove.objects.filter(
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


def _end_votes_collection_schedule():
    initiatives_objects = [
        x for x in initiatives.Initiative.objects.filter(
            state=initiatives.InitiativeState.VOTES_COLLECTION
        ) if x.vote_finish_date < timezone.now()
    ]
    for item in initiatives_objects:
        votes_count = initiatives.UserInitiativeApprove.objects.filter(
            initiative=item,
            timestamp__range=[
                item.votes_collection_begin_date,
                item.vote_finish_date
            ]
        ).count()
        with transaction.atomic():
            if votes_count < item.votes_threshold:
                item.time_exceeded()
            else:
                item.necessary_votes_collected()
            item.save()
