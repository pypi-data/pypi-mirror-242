import random
from string import ascii_letters, digits
from typing import Union

from django.db import transaction
from django.db.models import Q, QuerySet
from django.utils import timezone

from config.settings import settings as global_settings
from modules.core.models import User, ActiveCitizenModule
from modules.core.models.active_citizen_module import ActiveCitizenModuleEnum
from modules.ecology.exceptions import (
    UserError,
    UserParticipationError,
    UserPurchaseError,
)
from modules.ecology.models import (
    Event,
    ParticipationUserEvent,
    UserState,
    GoodsNServicesItem,
    UserPurchase,
    Notification,
    NotificationType,
    Settings,
)
from modules.ecology.models.participation_user_event import ParticipationStatus
from modules.ecology.models.user_purchase import PurchaseStatus
from modules.ecology.services.user_balance_operation import BalanceOperationService
from modules.ecology.tasks import (
    send_email_on_user_adding_initiative,
    send_email_on_user_approve_initiative,
    send_email_on_participation_vote,
)


class UserService:
    CODE_LENGTH = 5

    def __init__(self, user: User):
        if not user.is_simple_user:
            raise UserError("У пользователя нет роли обычного пользователя")
        if user.ecology.state == UserState.INITIAL:
            raise UserError("Пользователь не учавствует в программе")
        self.user = user

    def generate_code(self, length: int) -> str:
        letters = ascii_letters + digits
        code = "".join(random.choice(letters) for i in range(length))
        return code

    def get_participations(self) -> Union[QuerySet, ParticipationUserEvent]:
        return ParticipationUserEvent.objects.filter(participant=self.user).order_by(
            "-timestamp"
        )

    def get_purchases(self) -> Union[QuerySet, UserPurchase]:
        return UserPurchase.objects.filter(user=self.user).order_by("-timestamp")

    def event_participate(self, event: Event) -> UserPurchase:
        """Создает объект участия пользователя в предложении (мероприятии)"""
        if (
                event.maximum_participants
                and event.maximum_participants
                <= ParticipationUserEvent.objects.filter(
            event=event, status=ParticipationStatus.CONFIRMED
        ).count()
        ):
            raise UserParticipationError(
                "Достигнуто максимальное количество участников"
            )

        if (
                not event.multiple_participation
                and ParticipationUserEvent.objects.filter(
            participant=self.user, event=event, status=ParticipationStatus.CONFIRMED
        ).exists()
        ):
            raise UserParticipationError("Участие в этом предложении единоразовое")

        participation_user_event = ParticipationUserEvent.objects.filter(
            participant=self.user, event=event, status=ParticipationStatus.NOT_CONFIRMED
        ).first()

        if not participation_user_event:
            participation_user_event = ParticipationUserEvent.objects.create(
                participant=self.user, event=event
            )

        return participation_user_event

    @transaction.atomic
    def purchase(self, item: GoodsNServicesItem) -> UserPurchase:
        """Создает объект покупки пользователя"""
        if (
                item.maximum_purchasers
                and item.maximum_purchasers
                <= UserPurchase.objects.filter(
            Q(goods_n_services_item=item) & ~Q(status=PurchaseStatus.RETURNED)
        ).count()
        ):
            raise UserPurchaseError(
                "Достигнуто максимальное количество приобретений данного поощрения"
            )

        if (
                not item.multiple_purchase
                and UserPurchase.objects.filter(
            Q(user=self.user, goods_n_services_item=item)
            & ~Q(status=PurchaseStatus.RETURNED)
        ).exists()
        ):
            raise UserPurchaseError("Приобретение этого поощрения единоразовое")

        now_time = timezone.now()
        code = self.generate_code(self.CODE_LENGTH)

        user_purchase = UserPurchase.objects.create(
            user=self.user,
            goods_n_services_item=item,
            code=code,
            timestamp=now_time,
        )

        user_balance_operation = BalanceOperationService(self.user).charge_off_balance(
            amount=item.cost,
            purchase=user_purchase,
            earned_bonuses=False,
            reason="PURCHASE",
        )

        Notification.objects.create(
            user=self.user,
            timestamp=now_time,
            text=f'С вашего счета списано {item.cost} бонусов. Совершена покупка – "{item.name}"',
            type=NotificationType.GOODSNSERVICES_PURCHASE,
            user_balance_operation=user_balance_operation,
            user_purchase=user_purchase,
        )

        return user_purchase

    @transaction.atomic
    def return_purchase(self, purchase: UserPurchase) -> UserPurchase:
        """Совершает возврат покупки пользоваетелем"""
        now_time = timezone.now()
        if purchase.status != PurchaseStatus.NOT_CONFIRMED:
            raise UserError("Поощрение уже подтверждено или возвращено")

        if not purchase.goods_n_services_item.return_possibility:
            raise UserPurchaseError("Это поощрение нельзя вернуть")

        user_balance_operation = BalanceOperationService(self.user).add_balance(
            amount=purchase.goods_n_services_item.cost,
            earned_bonuses=False,
            reason=f"Возврат бонусов за поощрение {purchase.goods_n_services_item.name}",
            purchase=purchase,
        )

        Notification.objects.create(
            user=self.user,
            timestamp=now_time,
            text=f"Возврат бонусов за поощрение {purchase.goods_n_services_item.name}",
            type=NotificationType.RETURN_GOODSNSERVICES_PURCHASE,
            user_balance_operation=user_balance_operation,
            user_purchase=purchase,
        )
        purchase.status = PurchaseStatus.RETURNED
        purchase.save(update_fields=["status"])
        return purchase

    def add_bonuses_on_user_adding_initiative(self, initiative):
        ecology_stimulation_module = ActiveCitizenModule.objects.filter(
            name=ActiveCitizenModuleEnum.ECOLOGY_STIMULATION).first()
        ecology_offers_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.ECOLOGY_OFFERS).first()

        if ecology_stimulation_module and ecology_offers_module:
            bonus_program = ecology_stimulation_module.is_worked and ecology_offers_module.is_worked
        else:
            bonus_program = global_settings.BONUS_PROGRAM
        if not bonus_program:
            return

        settings: Settings = Settings.load()
        amount = settings.add_initiative_reward
        user_balance_operation = BalanceOperationService(self.user).add_balance(
            amount=amount,
            earned_bonuses=True,
            reason="Начисление бонусов за подачу инициативы",
        )

        Notification.objects.create(
            user=self.user,
            timestamp=timezone.now(),
            text=f"Начисление бонусов за подачу инициативы {initiative.title}",
            type=NotificationType.ADDING_INITIATIVE,
            user_balance_operation=user_balance_operation,
            initiative=initiative,
        )

        send_email_on_user_adding_initiative.delay(
            to=[self.user.email],
            initiative_name=initiative.title,
            reward=settings.add_initiative_reward,
        )

    def add_bonuses_on_user_approve_initiative(self, initiative):
        ecology_stimulation_module = ActiveCitizenModule.objects.filter(
            name=ActiveCitizenModuleEnum.ECOLOGY_STIMULATION).first()
        ecology_offers_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.ECOLOGY_OFFERS).first()

        if ecology_stimulation_module and ecology_offers_module:
            bonus_program = ecology_stimulation_module.is_worked and ecology_offers_module.is_worked
        else:
            bonus_program = global_settings.BONUS_PROGRAM
        if not bonus_program:
            return

        settings: Settings = Settings.load()
        amount = settings.approve_initiative_reward
        user_balance_operation = BalanceOperationService(self.user).add_balance(
            amount=amount,
            earned_bonuses=True,
            reason=f"Начисление бонусов за поддержку инициативы {initiative.title}",
        )

        Notification.objects.create(
            user=self.user,
            timestamp=timezone.now(),
            text=f"Начисление бонусов за поддержку инициативы {initiative.title}",
            type=NotificationType.APPROVE_INITIATIVE,
            user_balance_operation=user_balance_operation,
            initiative=initiative,
        )
        send_email_on_user_approve_initiative.delay(
            to=[self.user.email],
            initiative_name=initiative.title,
            reward=settings.approve_initiative_reward,
        )

    def add_bonuses_on_user_vote(self, vote):
        ecology_stimulation_module = ActiveCitizenModule.objects.filter(
            name=ActiveCitizenModuleEnum.ECOLOGY_STIMULATION).first()
        ecology_offers_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.ECOLOGY_OFFERS).first()

        if ecology_stimulation_module and ecology_offers_module:
            bonus_program = ecology_stimulation_module.is_worked and ecology_offers_module.is_worked
        else:
            bonus_program = global_settings.BONUS_PROGRAM
        if not bonus_program:
            return

        settings: Settings = Settings.load()

        amount = 0
        if not vote.not_bonus_eligible and not vote.bonus_amount:
            amount = settings.vote_reward
        elif not vote.not_bonus_eligible and vote.bonus_amount:
            amount = vote.bonus_amount

        if amount > 0:
            user_balance_operation = BalanceOperationService(self.user).add_balance(
                amount=amount,
                earned_bonuses=True,
                reason="Начисление бонусов за Участие в голосовании",
            )

            Notification.objects.create(
                user=self.user,
                timestamp=timezone.now(),
                text=f"Начисление бонусов за Участие в голосовании {vote.name}",
                type=NotificationType.VOTING_PARTICIPATION,
                user_balance_operation=user_balance_operation,
                vote=vote,
            )

            send_email_on_participation_vote.delay(
                to=[self.user.email], vote_name=vote.name, reward=settings.vote_reward
            )
