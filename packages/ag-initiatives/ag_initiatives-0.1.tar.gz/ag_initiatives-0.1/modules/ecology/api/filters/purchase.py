from typing import Union

import django_filters
from django.db.models import QuerySet, Q
from pydantic import ValidationError

from modules.ecology.models import UserPurchase
from modules.ecology.models.user_purchase import PurchaseStatus


class UserPurchaseFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method="filter_status")

    def filter_status(
        self, queryset: Union[QuerySet, UserPurchase], name: str, value: str
    ) -> Union[QuerySet, UserPurchase]:
        if "," not in value:
            return queryset.filter(status=value.upper())
        query = Q()
        status_string_list = value.split(",")
        for status in status_string_list:
            if status.upper() in PurchaseStatus.RESOLVER.keys():
                query |= Q(status=status)
            else:
                raise ValidationError("Некорректный фильтр статуса")
        return queryset.filter(query)
