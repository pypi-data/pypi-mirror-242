from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from modules.core.models import User
from modules.core.models.permissions import ModulesPermissions
from modules.core.services.operator_lko import OperatorLkoService
from modules.ecology.models import (
    ParticipationUserEvent,
    Event,
    Notification,
    NotificationType,
)
from modules.ecology.models.participation_user_event import ParticipationStatus
from modules.ecology.exceptions import OrganizerError
from modules.ecology.tasks import send_email_on_participation_event
from modules.ecology.services.user_balance_operation import BalanceOperationService


class OrganizerService:
    def __init__(self, organizer: User):
        if not organizer.is_operator:
            raise OrganizerError("Переданный пользователь не является организатором")
        if not organizer.sub_permissions.operator_permissions.department:
            raise OrganizerError("У данного организатора не указана организация")
        self.organizer = organizer
        self.service_class = OperatorLkoService

    def get_users_participation(self):
        """Возвращает queryset объект, с участиями пользователей в меропирятиях, отфильтрованный по организации и
        статусу участия"""
        service = self.service_class(user=self.organizer, module=ModulesPermissions.SUGGESTIONS)
        queryset = ParticipationUserEvent.objects.filter(
            (Q(event__locality__isnull=True) |
             Q(event__locality__in=service.get_allowed_localities()))
            & ~Q(status=ParticipationStatus.NOT_CONFIRMED)
            & Q(event__category__in=service.get_allowed_categories())
        ).order_by("-timestamp")
        return queryset

    @transaction.atomic
    def confirm_or_decline_participation(
        self, participation: ParticipationUserEvent, participation_status
    ) -> ParticipationUserEvent:
        if participation_status not in ParticipationStatus.RESOLVER.keys():
            raise OrganizerError("Неккоректный статус участия")
        lko_department = self.organizer.operator_permissions.department
        if lko_department != participation.event.organization:
            raise OrganizerError(
                "Организатор не является организатором данного предложения"
            )

        if participation.status != ParticipationStatus.NOT_CONFIRMED:
            raise OrganizerError("Участие уже подтверждено или отклонено")

        event: Event = participation.event
        participant: User = participation.participant

        now_time = timezone.now()

        participation.status = participation_status
        participation.confirmation_timestamp = now_time
        participation.save()

        if participation.status == ParticipationStatus.CONFIRMED:
            reward = event.reward

            balance_operation = BalanceOperationService(participant).add_balance(
                amount=reward,
                reason="Участие пользователя в мероприятии",
                participation=participation,
            )

            Notification.objects.create(
                user=participant,
                timestamp=now_time,
                type=NotificationType.EVENT_PARTICIPATION,
                text=f'На ваш счет зачислено {event.reward} бонусов. Подтверждено участие в предложении – "{event.name}"',
                user_balance_operation=balance_operation,
                participation=participation,
            )

            send_email_on_participation_event.delay(
                to=[participant.email],
                event_name=event.name,
                reward=reward,
            )

        elif participation.status == ParticipationStatus.DECLINED:
            Notification.objects.create(
                user=participant,
                timestamp=now_time,
                type=NotificationType.DECLINE_EVENT_PARTICIPATION,
                text=f'Вам отклонили участие в предложении – "{event.name}"',
                participation=participation,
            )

        return participation
