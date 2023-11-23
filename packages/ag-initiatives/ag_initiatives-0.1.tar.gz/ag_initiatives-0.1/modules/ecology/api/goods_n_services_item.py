from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.ecology.api.filters import GoodsNServicesItemFilter
from modules.ecology.api.serializers import (
    GoodsNServicesItemListSerializer,
    GoodsNServicesItemDetailsSerializer,
)
from modules.ecology.models import GoodsNServicesItem
from django_filters import rest_framework as filters


class GoodsNServicesItemAPI(viewsets.ReadOnlyModelViewSet):
    queryset = GoodsNServicesItem.objects.filter(is_published=True)
    serializer_class = GoodsNServicesItemListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = GoodsNServicesItemFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GoodsNServicesItemDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})
