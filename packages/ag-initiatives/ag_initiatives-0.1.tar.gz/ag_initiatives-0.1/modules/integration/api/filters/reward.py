import django_filters
from django.db.models import Q

from modules.ecology.models import GoodsNServicesItem, UserPurchase
from modules.ecology.models.user_purchase import PurchaseStatus


class RewardFilter(django_filters.FilterSet):
    maximum_purchase_usage = django_filters.BooleanFilter(
        method='filter_by_maximum_purchase_usage'
    )

    class Meta:
        model = GoodsNServicesItem
        fields = ['multiple_purchase']

    @staticmethod
    def filter_by_maximum_purchase_usage(queryset, _, value):
        # TODO Переделать фильтрацию, экстра фикс !!!!!
        res_pks = []
        for item in queryset:
            total_count = UserPurchase.objects.filter(
                Q(goods_n_services_item__id=item.id) & ~Q(status=PurchaseStatus.RETURNED)).count()
            if (value and item.maximum_purchasers and total_count >= item.maximum_purchasers) or (
                    not value and (not item.maximum_purchasers or item.maximum_purchasers <= total_count)):
                res_pks.append(item.id)
        return queryset.filter(id__in=res_pks)
