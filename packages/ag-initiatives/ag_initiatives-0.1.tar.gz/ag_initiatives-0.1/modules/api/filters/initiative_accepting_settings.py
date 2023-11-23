import django_filters
from django.db.models import Q

from modules.initiatives.models import (
    InitiativeAcceptingSettings,
)


class InitiativeAcceptingSettingsFilter(django_filters.FilterSet):
    municipalities = django_filters.CharFilter(method='filter_municipalities')
    localities = django_filters.CharFilter(method='filter_localities')
    categories = django_filters.CharFilter(method='filter_categories')
    subcategories = django_filters.CharFilter(method='filter_subcategories')
    type = django_filters.CharFilter(method='filter_type')

    class Meta:
        model = InitiativeAcceptingSettings
        fields = [
            "municipalities",
            "localities",
            "categories",
            "subcategories",
            "type",
            "active",
        ]

    def filter_municipalities(self, queryset, _, value):
        municipalities = value.split(',')
        return queryset.filter(
            Q(locality__in=municipalities) |
            Q(locality__parent__in=municipalities)
        )

    def filter_localities(self, queryset, _, value):
        localities = value.split(',')
        return queryset.filter(
            Q(locality__in=localities) |
            Q(locality__localities__in=localities)
        )

    def filter_categories(self, queryset, _, value):
        categories = value.split(',')
        return queryset.filter(
            Q(category__in=categories) |
            Q(category__parent__in=categories)
        )

    def filter_subcategories(self, queryset, _, value):
        subcategories = value.split(',')
        return queryset.filter(
            Q(category__in=subcategories) |
            Q(category__children__in=subcategories)
        )

    def filter_type(self, queryset, _, value):
        return queryset.filter(type__in=value.split(','))
