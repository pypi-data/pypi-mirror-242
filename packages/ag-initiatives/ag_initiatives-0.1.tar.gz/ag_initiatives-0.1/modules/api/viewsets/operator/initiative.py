from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from modules.api.filters import InitiativeFilter
from modules.api.pagination import DefaultPagination
from modules.api.permissions import IsInitiativeOperator
from modules.core.models import User
from modules.initiatives.models import InitiativeState
from .serializers import InitiativeForOperatorSerializer


class InitiativeOperatorAPI(ReadOnlyModelViewSet):
    """API Инициативы Оператора"""

    serializer_class = InitiativeForOperatorSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InitiativeFilter
    pagination_class = DefaultPagination
    permission_classes = [IsInitiativeOperator]

    def get_queryset(self):
        user: User = self.request.user
        queryset = user.operator_all_initiatives_for_view\
            .order_by("sort_field", "-creation_date_time")
        return queryset

    @action(methods=["get"], detail=False, url_path="info")
    def info(self, request: Request, *args, **kwargs):
        data = {
            "state": InitiativeState.RESOLVER.values()
        }
        return Response(data)

    @action(methods=["get"], detail=False)
    def count(self, request: Request):
        queryset = self.get_queryset()
        return Response({"count": queryset.count()})
