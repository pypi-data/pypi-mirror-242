from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.api.filters import InitiativeAcceptingSettingsFilter
from modules.api.pagination import DefaultPagination
from modules.api.permissions import IsOperator
from modules.api.serializers import LocalityShortSerializer, InitiativeCategoryNameSerializer
from modules.api.viewsets import (
    InitiativeAcceptingSettingsViewSet
)
from modules.api.viewsets.admin_lko.serializers.department import get_divided_municipalities_data, \
    get_municipalities_with_unavailable_from_localities
from modules.core.models.permissions import ModulesPermissions
from modules.core.services.curator import CuratorService
from modules.initiatives.models import InitiativeCategory, InitiativeAcceptingSettings


class CuratorInitiativeSettingsAPI(InitiativeAcceptingSettingsViewSet):
    permission_classes = (IsOperator,)
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InitiativeAcceptingSettingsFilter
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'sub_permissions'):
            permissions = user.sub_permissions.curator_permissions.select_related(
                'department',
            ).prefetch_related(
                'voting_municipalities', 'voting_localities',
            ).filter(
                modules_permissions__contains=ModulesPermissions.INITIATIVES
            )
            query = Q()
            for permission in permissions:
                localities = (
                        permission.initiatives_municipalities.values_list(
                            'id', flat=True) |
                        permission.initiatives_localities.values_list(
                            'id', flat=True)
                )
                categories = permission.initiatives_categories.values_list(
                    'id', flat=True)
                query |= Q(
                    department=permission.department,
                    locality__in=localities,
                ) & Q(
                    Q(category__in=categories) |
                    Q(category__parent__in=categories)
                )

            return self.queryset.filter(query).distinct()

        return InitiativeAcceptingSettings.objects.none()

    @action(methods=["get"], detail=False)
    def filters(self, request, *args, **kwargs):
        data = {
            'municipalities': [],
            'localities': [],
            'categories': [],
            'subcategories': [],
        }
        operator = CuratorService(
            user=self.request.user,
            module=ModulesPermissions.INITIATIVES,
        )

        municipalities = set()
        for i in operator.get_allowed_localities():
            if i.is_locality:
                data['localities'].append(
                    LocalityShortSerializer(i).data)
                municipalities.add(i.parent)
            elif i.is_municipality:
                municipalities.add(i)
        data['municipalities'] = LocalityShortSerializer(
            municipalities, many=True).data

        categories = set()
        subcategories = set()
        for i in operator.get_allowed_categories():
            if i.parent:
                subcategories.add(i)
                categories.add(i.parent)
            else:
                categories.add(i)
                subcategories |= set(i.children.all())
        data['categories'] = InitiativeCategoryNameSerializer(
            categories, many=True).data
        data['subcategories'] = InitiativeCategoryNameSerializer(
            subcategories, many=True).data

        return Response(data)

    @action(methods=["get"], detail=False)
    def info(self, request, *args, **kwargs):
        operator = CuratorService(
            user=self.request.user,
            module=ModulesPermissions.INITIATIVES
        )
        data = {
            'localities': get_divided_municipalities_data(
                get_municipalities_with_unavailable_from_localities(
                    operator.get_allowed_localities()
                )
            ),
            'categories': []
        }
        all_categories = operator.get_allowed_categories()
        categories = all_categories.filter(parent__isnull=True)
        for category in categories:
            subcategories = all_categories.filter(parent=category)
            if not subcategories:
                subcategories = category.children.all()

            category_data = InitiativeCategoryNameSerializer(category).data
            category_data['subcategories'] = InitiativeCategoryNameSerializer(
                subcategories, many=True
            ).data
            data['categories'].append(category_data)

        categories = InitiativeCategory.objects.filter(
            children__in=all_categories.filter(parent__isnull=False)).distinct()
        for category in categories:
            category_data = InitiativeCategoryNameSerializer(category).data
            category_data['subcategories'] = InitiativeCategoryNameSerializer(
                all_categories.filter(parent=category), many=True
            ).data
            data['categories'].append(category_data)

        return Response(data)
