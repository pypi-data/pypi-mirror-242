from django.core.management.base import BaseCommand

from modules.initiatives.models import Initiative, InitiativeState
from modules.initiatives.tasks import end_votes_collection


class Command(BaseCommand):
    def handle(self, *args, **options):
        initiatives = Initiative.objects.filter(state=InitiativeState.VOTES_COLLECTION)
        for initiative in initiatives:
            end_votes_collection.apply_async(
                kwargs={"pk": initiative.pk}, eta=initiative.vote_finish_date
            )
