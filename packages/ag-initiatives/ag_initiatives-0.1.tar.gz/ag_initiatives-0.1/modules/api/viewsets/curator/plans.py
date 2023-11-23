from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.pagination import DefaultPagination
from modules.api.viewsets.curator.permissions import IsPlanCurator
from modules.core.models.permissions import ModulesPermissions
from modules.core.services.curator import CuratorService
from modules.plans.api.filters import PlanFilter
from modules.plans.api.serializers import PlanListSerializer, PlanDetailsSerializer
from modules.plans.models import Plan


class CuratorPlansApi(viewsets.ReadOnlyModelViewSet):

    pagination_class = DefaultPagination
    permission_classes = [IsPlanCurator]
    filterset_class = PlanFilter

    def get_curator_service(self) -> CuratorService:
        return CuratorService(self.request.user)

    def get_queryset(self):
        service = self.get_curator_service()
        queryset = service.get_allowed_objects(module=ModulesPermissions.PLANS)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PlanListSerializer
        elif self.action == "retrieve":
            return PlanDetailsSerializer

    @action(methods=["get"], detail=False)
    def count(self, request: Request) -> Response:
        return Response({
            "count": self.filter_queryset(self.get_queryset()).count()
        })
