from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.viewsets.curator.permissions import IsVotingCurator
from modules.voting.api.filters import VoteFilter
from modules.api.pagination import DefaultPagination
from modules.api.serializers import VoteSerializer, VoteDetailsSerializer
from modules.core.models.permissions import ModulesPermissions
from modules.core.services.curator import CuratorService


class CuratorVotingApi(viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsVotingCurator]
    pagination_class = DefaultPagination
    filterset_class = VoteFilter

    def get_curator_service(self) -> CuratorService:
        return CuratorService(self.request.user)

    def get_queryset(self):
        return self.get_curator_service().get_allowed_objects(ModulesPermissions.VOTING)

    def get_serializer_class(self):
        if self.action == "list":
            return VoteSerializer
        elif self.action == "retrieve":
            return VoteDetailsSerializer

    @action(methods=["get"], detail=False)
    def count(self, request: Request) -> Response:
        return Response({
            "count": self.filter_queryset(self.get_queryset()).count()
        })
