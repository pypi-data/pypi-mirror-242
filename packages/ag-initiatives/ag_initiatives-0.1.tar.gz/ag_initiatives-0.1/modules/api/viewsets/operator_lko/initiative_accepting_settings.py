from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.api.filters import InitiativeAcceptingSettingsFilter
from modules.api.pagination import DefaultPagination
from modules.api.permissions import IsOperator
from modules.api.serializers import InitiativeCategoryNameSerializer, LocalityShortSerializer
from modules.api.viewsets import InitiativeAcceptingSettingsViewSet
from modules.api.viewsets.operator_lko.serializers import (
    InitiativeSettingsWriteSerializer
)
from modules.api.viewsets.operator_lko.serializers.locality import (
    MunicipalityWithUnavailableTreeSerializer
)
from modules.core.models.permissions import ModulesPermissions
from modules.core.services.operator_lko import OperatorLkoService
from modules.initiatives.models import InitiativeAcceptingSettings


class InitiativeSettingsOperatorLkoAPI(InitiativeAcceptingSettingsViewSet):
    permission_classes = (IsOperator,)
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InitiativeAcceptingSettingsFilter
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'sub_permissions'):
            permission = user.sub_permissions.operator_permissions
            if ModulesPermissions.INITIATIVES not in permission.modules_permissions:
                return QuerySet()
            localities = (
                    permission.initiatives_municipalities.values_list(
                        'id', flat=True) |
                    permission.initiatives_localities.values_list(
                        'id', flat=True)
            )
            categories = permission.initiatives_categories.values_list(
                'id', flat=True)
            return self.queryset.filter(
                Q(
                    department=permission.department,
                    locality__in=localities,
                ) & Q(
                    Q(category__in=categories) |
                    Q(category__parent__in=categories)
                )
            ).order_by('-id').distinct()

        return InitiativeAcceptingSettings.objects.none()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return super(
                InitiativeAcceptingSettingsViewSet, self
            ).get_serializer_class()
        return InitiativeSettingsWriteSerializer

    @action(methods=["get"], detail=False)
    def filters(self, request, *args, **kwargs):
        data = {
            'municipalities': [],
            'localities': [],
            'categories': [],
            'subcategories': [],
        }
        operator = OperatorLkoService(
            user=self.request.user,
            module=ModulesPermissions.INITIATIVES
        )

        municipalities = set()
        for i in operator.get_allowed_localities():
            if i.is_locality:
                data['localities'].append(
                    LocalityShortSerializer(i).data)
                if i.parent is not None:
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
        operator = OperatorLkoService(
            user=self.request.user,
            module=ModulesPermissions.INITIATIVES
        )
        data = {
            'localities': {
                "municipal_regions": [],
                "municipal_districts": [],
                "urban_districts": MunicipalityWithUnavailableTreeSerializer(request.user.sub_permissions.operator_permissions.initiatives_localities.all(), many=True).data
            },
            'categories': []
        }
        all_categories = operator.get_allowed_categories()
        for category in all_categories:
            if not category.parent:
                category_data = InitiativeCategoryNameSerializer(category).data
                subcategories = all_categories.filter(parent=category)
                category_data['subcategories'] = InitiativeCategoryNameSerializer(
                    subcategories, many=True
                ).data
                data['categories'].append(category_data)

        return Response(data)
