import json

from rest_framework import viewsets, status

from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.appeals.api import AppealOperatorAPI, AppealModeratorAPI, AppealUserAPI
from modules.appeals.api.filters import AppealFilter
from modules.appeals.api.serializers import (
    AppealListSerializer,
    AppealDetailsSerializer,
    AppealResponseSerializer,
)
from modules.appeals.models import Appeal, AppealState

from django.core.serializers import serialize, deserialize

from modules.appeals.services.mail_service import MailService
from modules.core.permissions import IsUser, IsOperator, IsModerator


class AppealAPI(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Appeal.objects.filter(
            is_public=True,
            state__in=[
                AppealState.MODERATION_ACCEPTED,
                AppealState.IN_PROGRESS,
                AppealState.RESPONDED,
            ],
        )
        .select_related("category", "category__parent")
        .order_by("-creation_date_time")
    )

    serializer_class = AppealListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AppealFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AppealDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @action(methods=["get"], detail=False)
    def map(self, request):

        appeals = self.filter_queryset(self.get_queryset())

        # сериализатор GeoJSON записывает координаты в формате [широта, долгота],
        # когда для geojson координаты должны быть в формате [долгота, широта]
        # соответственно этому, потребитель данных api должен это учитывать
        geojson = serialize(
            "geojson",
            appeals,
            geometry_field="gis_point",
            fields=["pk", "state", "category"],
            srid=4326,
        )
        return Response(json.loads(geojson))

    @action(
        methods=["get"],
        detail=True,
        url_path="notifications",
        permission_classes=[IsOperator | IsModerator | IsUser],
    )
    def item_notifications(self, request, pk):
        appeals_api_cls = None
        if request.user.is_operator:
            appeals_api_cls = AppealOperatorAPI
        elif request.user.is_moderator:
            appeals_api_cls = AppealModeratorAPI
        elif request.user.is_simple_user:
            appeals_api_cls = AppealUserAPI
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return appeals_api_cls.as_view({"get": "item_notifications"})(
            request._request, pk=pk
        )

    @action(methods=["get"], detail=True)
    def response(self, request, pk):
        instance: Appeal = self.get_object()
        try:
            return Response(AppealResponseSerializer(instance.response).data)
        except Appeal.response.RelatedObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
