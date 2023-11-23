from django.db.models import Q
from django.utils import timezone

from modules.initiatives import models as initiatives


class InitiativeStateChanger:
    def __init__(self, initiative, user=None):
        self.initiative = initiative
        self.user = user

    def create_initiative_state_change(self, **kwargs):
        initiatives.InitiativeStateChange.objects.create(
            initiative=self.initiative,
            user=self.user,
            new_state=kwargs["new_state"],
            timestamp=timezone.now(),
        )

    def create_initiative_communication(self, is_system_notification=False, **kwargs):
        files = None
        if "files" in kwargs:
            files = kwargs.pop("files")
        communication = initiatives.InitiativeOperatorCommunication.objects.create(
            initiative=self.initiative,
            user=self.user if not is_system_notification else None,
            timestamp=timezone.now(),
            **kwargs
        )
        if files:
            communication.files.set(files)

    def mark_offered_changes_as_viewed(self, **kwargs):
        communication = self.initiative.communications.filter(
            type=kwargs.get("type")
        ).last()
        if communication:
            communication.user_viewed = True
            communication.save()
