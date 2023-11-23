import json

from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.plans.api.filters import PlanFilter
from modules.plans.api.serializers import (
    PlanListSerializer,
    PlanDetailsSerializer,
    LocationMapSerializer,
    PlanCommentModeratorListSerializer,
    PlanCommentModeratorSerializer,
)
from modules.plans.models import Plan, Location
from django.core.serializers import serialize, deserialize


class PlanAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.none()
    serializer_class = PlanListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PlanFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Plan.objects.filter(publication_date__lte=timezone.now()).order_by(
            "-publication_date"
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlanDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @action(methods=["get"], detail=False)
    def map(self, request):
        plans = self.filter_queryset(self.get_queryset())

        locations = Location.objects.filter(
            plan__in=plans.values_list("id", flat=True), gis_point__isnull=False
        )

        return Response(LocationMapSerializer(locations, many=True).data)

    @action(methods=["get"], detail=True)
    def comments(self, request, pk=None, *args, **kwargs):
        plan: Plan = self.get_object()
        return Response(
            PlanCommentModeratorSerializer(
                plan.comments.filter(moderated=True), many=True
            ).data,
            status=status.HTTP_200_OK,
        )
