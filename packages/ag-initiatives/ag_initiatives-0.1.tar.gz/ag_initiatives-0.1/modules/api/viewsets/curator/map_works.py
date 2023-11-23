from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.pagination import DefaultPagination
from modules.api.viewsets.curator.permissions import IsMapWorksCurator
from modules.core.models.permissions import ModulesPermissions
from modules.core.services.curator import CuratorService
from modules.map_works.api.filters import WorksFilter
from modules.map_works.api.serializers import WorksListSerializer, WorksDetailsSerializer


class CuratorMapWorksApi(viewsets.ReadOnlyModelViewSet):
    pagination_class = DefaultPagination
    permission_classes = [
        IsAuthenticated,
        IsMapWorksCurator,
    ]
    filterset_class = WorksFilter

    def get_curator_service(self) -> CuratorService:
        return CuratorService(self.request.user)

    def get_queryset(self):
        service = self.get_curator_service()
        return service.get_allowed_objects(module=ModulesPermissions.MAP_WORKS)

    def get_serializer_class(self):
        if self.action == "list":
            return WorksListSerializer
        elif self.action == "retrieve":
            return WorksDetailsSerializer

    @action(methods=["get"], detail=False)
    def count(self, request: Request) -> Response:
        return Response({
            "count": self.filter_queryset(self.get_queryset()).count()
        })
