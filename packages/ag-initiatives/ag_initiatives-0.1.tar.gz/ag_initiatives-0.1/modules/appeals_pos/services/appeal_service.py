import logging
from typing import Union

from django.db import transaction
from django.db.models import QuerySet

from modules.appeals.models import AppealState
from modules.appeals_pos.models import Appeal
from modules.core.models import User
from .smev.pos_smev_service import PosSmevService

logger = logging.getLogger("appeal service")


class AppealService:
    pos_smev_service = PosSmevService()

    @staticmethod
    def get_user_appeals(user: User) -> Union[QuerySet, Appeal]:
        return Appeal.objects.filter(user=user).order_by("-creation_date_time")

    @staticmethod
    def get_published_appeals() -> Union[QuerySet, Appeal]:
        return Appeal.objects.filter(
            to_publish=True,
            status__in=[
                AppealState.MODERATION_ACCEPTED,
                AppealState.RESPONDED,
                AppealState.IN_PROGRESS,
            ],
        ).order_by("-creation_date_time")

    @transaction.atomic
    def save_appeal(self, appeal: Appeal):
        response = self.pos_smev_service.add_appeal(appeal)
        return response
