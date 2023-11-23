from django.utils import timezone

from modules.core.models import User
from modules.ecology.models import (
    UserBalanceOperation,
    UserBalanceOperationType,
    ParticipationUserEvent,
    UserPurchase,
)
from modules.ecology.exceptions import BalanceOperationError


class BalanceOperationService:
    def __init__(self, user: User):
        if not user.is_simple_user:
            raise BalanceOperationError("У пользователя нет роли простого пользователя")
        self.user = user
        self.ecology_profile = user.ecology_profile

    def add_balance(
        self,
        amount: int,
        reason: str,
        earned_bonuses: bool = True,
        participation: ParticipationUserEvent = None,
        purchase: UserPurchase = None,
    ) -> UserBalanceOperation:
        now_time = timezone.now()
        update_fields = ["balance"]

        self.ecology_profile.balance += amount

        if earned_bonuses:
            self.user.ecology_profile.earned_bonuses += amount
            update_fields.append("earned_bonuses")

        self.ecology_profile.save(update_fields=update_fields)

        return UserBalanceOperation.objects.create(
            user=self.user,
            amount=amount,
            timestamp=now_time,
            type=UserBalanceOperationType.INCOME,
            reason=reason,
            participation=participation,
            purchase=purchase,
        )

    def charge_off_balance(
        self,
        amount: int,
        reason: str,
        participation: ParticipationUserEvent = None,
        earned_bonuses: bool = True,
        purchase: UserPurchase = None,
    ) -> UserBalanceOperation:

        now_time = timezone.now()
        update_fields = ["balance"]

        if self.ecology_profile.balance < amount:
            raise BalanceOperationError("Недостаточно средств")

        self.ecology_profile.balance -= amount

        if earned_bonuses:
            self.ecology_profile.earned_bonuses -= amount
            update_fields.append("earned_bonuses")

        self.ecology_profile.save(update_fields=update_fields)

        return UserBalanceOperation.objects.create(
            user=self.user,
            amount=amount,
            timestamp=now_time,
            type=UserBalanceOperationType.EXPENSE,
            reason=reason,
            participation=participation,
            purchase=purchase,
        )
