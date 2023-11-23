from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.pagination import DefaultPagination
from modules.api.viewsets.filters import UserFilter
from modules.api.viewsets.curator.serializers.user import CuratorUserShortSerializer, CuratorUserDetailSerializer
from modules.core.models import User
from modules.core.permissions import IsOperator
from modules.core.services.curator import CuratorService


class UserManagerApi(viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsOperator]
    pagination_class = DefaultPagination
    serializer_class = CuratorUserShortSerializer
    filterset_class = UserFilter

    def get_curator_service(self, user: User) -> CuratorService:
        return CuratorService(user)

    def get_serializer_class(self):
        if self.action == "list":
            return CuratorUserShortSerializer
        elif self.action == "retrieve":
            return CuratorUserDetailSerializer

    def get_queryset(self):
        queryset = self.get_curator_service(self.request.user).get_allowed_users()
        order_by_param = self.request.query_params.get("order_by", None)

        if order_by_param is None:
            return queryset
        return queryset.order_by(order_by_param)

    @action(methods=["get"], detail=False)
    def count(self, request: Request) -> Response:
        return Response({
            "count": self.filter_queryset(self.get_queryset()).count()
        })
