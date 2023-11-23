from django.db.models import Q

from modules.core.models import User
from modules.core.models.permissions import ModulesPermissions
from modules.core.services.operator_lko import OperatorLkoService
from modules.ecology.exceptions import PartnerError
from modules.ecology.models import UserBalanceOperation, UserPurchase
from modules.ecology.models.user_purchase import PurchaseStatus
from modules.ecology.tasks import send_email_on_purchase_confirm


class PartnerService:
    def __init__(self, partner: User):
        if not partner.is_operator:
            raise PartnerError("Данный пользователь не является партнером")
        self.partner = partner
        self.service_class = OperatorLkoService

    def get_history(self):
        """Получает историю операций с поощрениями, где организация совпадает с организацией партнера"""
        service = self.service_class(user=self.partner, module=ModulesPermissions.ENCOURAGEMENTS)
        lko_department = self.partner.operator_permissions.department
        queryset = (
            UserBalanceOperation.objects.filter(
                (Q(purchase__goods_n_services_item__locality__isnull=True) |
                 Q(purchase__goods_n_services_item__locality__in=service.get_allowed_localities())),
                Q(purchase__goods_n_services_item__category__in=service.get_allowed_categories()),
                Q(purchase__goods_n_services_item__organization=lko_department)
            )
            .select_related("purchase")
            .select_related("purchase__goods_n_services_item")
            .order_by("-timestamp").distinct()
        )
        return queryset

    def get_users_purchases(self):
        """Получает queryset необработанных заявок на подтверждение получения поощрения"""
        service = self.service_class(user=self.partner, module=ModulesPermissions.ENCOURAGEMENTS)
        lko_department = self.partner.operator_permissions.department
        queryset = (
            UserPurchase.objects.filter(
                (Q(goods_n_services_item__locality__isnull=True) |
                 Q(goods_n_services_item__locality__in=service.get_allowed_localities())),
                Q(status=PurchaseStatus.NOT_CONFIRMED),
                Q(goods_n_services_item__category__in=service.get_allowed_categories()),
                Q(goods_n_services_item__organization=lko_department)
            )
            .select_related("goods_n_services_item")
            .order_by("-timestamp").distinct()
        )
        return queryset

    def confirm_purchase(self, purchase: UserPurchase, code: str) -> UserPurchase:
        """Подтверждение получения поощрения пользователем"""
        lko_department = self.partner.operator_permissions.department
        if lko_department != purchase.goods_n_services_item.organization:
            raise PartnerError("Партнер не является партнером для данного поощрения")

        if purchase.status != PurchaseStatus.NOT_CONFIRMED:
            raise PartnerError("Поощрение уже подтверждено или отклонено")

        if code != purchase.code:
            raise PartnerError("Код подтверждения не совпадает")

        purchase.status = PurchaseStatus.CONFIRMED
        purchase.save(update_fields=["status"])

        item = purchase.goods_n_services_item

        send_email_on_purchase_confirm.delay(
            to=[purchase.user.email], reward_name=item.name, cost=item.cost
        )

        return purchase
