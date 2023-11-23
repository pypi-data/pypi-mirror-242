from django.db.models import Prefetch, Q
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from modules.api.filters import InitiativeFilter
from modules.api.pagination import DefaultPagination
from modules.api.serializers import InitiativeSerializer, LocalitySerializer
from modules.core.models import User, Locality
from modules.core.models.permissions import ModulesPermissions
from modules.core.permissions import IsOperator
from modules.core.services.operator_lko import OperatorLkoService
from modules.initiatives.models import Initiative, InitiativeState


class InitiativeOperatorLkoAPI(ReadOnlyModelViewSet):
    """API Инициативы Оператора ЛКО"""

    permission_classes = [IsOperator]
    service_class = OperatorLkoService
    serializer_class = InitiativeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InitiativeFilter
    pagination_class = DefaultPagination

    def get_queryset(self):
        user: User = self.request.user
        return Initiative.objects.filter(
            Q(
                locality__in=user.sub_permissions.operator_permissions.initiatives_localities.all(),
                settings__department=user.sub_permissions.operator_permissions.department,
                state__in=[
                    InitiativeState.REJECTED,
                    InitiativeState.REJECTED_VOTES_THRESHOLD,
                    InitiativeState.MODERATION,
                    InitiativeState.VOTES_COLLECTION,
                    InitiativeState.CONSIDERATION,
                    InitiativeState.ACCOMPLISHED,
                    InitiativeState.IN_PROGRESS,
                ]
            ) & (
                Q(category__in=user.sub_permissions.operator_permissions.initiatives_categories.all()) |
                Q(category__parent__in=user.sub_permissions.operator_permissions.initiatives_categories.all())
            )
        ).prefetch_related(
            Prefetch(
                'locality',
                queryset=Locality.objects.select_related('parent').all()
            )
        ).distinct().order_by("-creation_date_time")

    @action(methods=["get"], detail=False, url_path="info")
    def info(self, request: Request, *args, **kwargs):
        user: User = request.user
        service = self.service_class(user=user, module=ModulesPermissions.INITIATIVES)
        data = {
            "state": dict(InitiativeState.CHOICES),
            "localities": LocalitySerializer(service.get_allowed_localities(), many=True).data,
        }
        return Response(data)

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})
