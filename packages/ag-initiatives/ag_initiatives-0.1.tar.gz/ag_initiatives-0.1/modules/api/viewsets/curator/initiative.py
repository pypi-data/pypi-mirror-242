from django.db.models import Q, Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.filters import InitiativeFilter
from modules.api.pagination import DefaultPagination
from modules.api.serializers import InitiativeSerializer, InitiativeShortSerializer
from modules.core.models import Locality
from modules.core.models.permissions import ModulesPermissions
from modules.core.permissions import IsOperator
from modules.core.services.curator import CuratorService
from modules.initiatives.enums import InitiativeState
from modules.initiatives.models import Initiative


class CuratorInitiativeApi(viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsOperator]
    service_class = CuratorService
    pagination_class = DefaultPagination
    serializer_class = InitiativeSerializer
    filterset_class = InitiativeFilter

    def get_curator_service(self) -> CuratorService:
        return CuratorService(self.request.user)

    def get_queryset(self):
        user = self.request.user
        service = self.service_class(
            user=user, module=ModulesPermissions.INITIATIVES)
        return Initiative.objects.filter(
            Q(
                locality__in=service.get_allowed_localities(),
                settings__department__in=service.get_allowed_departments(),
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
                    Q(category__in=service.get_allowed_categories()) |
                    Q(category__parent__in=service.get_allowed_categories())
            )
        ).prefetch_related(
            Prefetch(
                'locality',
                queryset=Locality.objects.select_related('parent').all()
            )
        ).distinct().order_by("-creation_date_time")

    @action(methods=["get"], detail=False)
    def count(self, request: Request) -> Response:
        return Response({
            "count": self.filter_queryset(self.get_queryset()).count()
        })
