from rest_framework import viewsets, status, mixins
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.pagination import DefaultPagination
from modules.core.permissions import IsAdminLKO, IsOperator
from modules.voting.api.filters import LocalVotingGroupFilter
from modules.voting.api.serializers.local_voting_group_serializer import (
    LocalVotingGroupSerializer,
    LocalVotingGroupCreateSerializer,
)
from modules.voting.models import LocalVotingGroup, VotingParticipant


class LocalVotingGroupAPI(
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet
):
    queryset = LocalVotingGroup.objects.all().prefetch_related("participants")
    serializer_class = LocalVotingGroupSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = LocalVotingGroupFilter
    permission_classes = [IsAdminLKO | IsOperator]
    pagination_class = DefaultPagination

    def get_queryset(self):
        order_by_param = self.request.query_params.get("order_by", None)
        if order_by_param is None:
            return self.queryset
        return self.queryset.order_by(order_by_param)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LocalVotingGroupSerializer
        elif self.action in ["create", "update"]:
            return LocalVotingGroupCreateSerializer

    def create(self, request: Request) -> Response:
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        return Response(LocalVotingGroupSerializer(group).data)

    def update(self, request: Request, pk: int) -> Response:

        try:
            instance = self.queryset.get(pk=pk)
        except LocalVotingGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer_class()(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

