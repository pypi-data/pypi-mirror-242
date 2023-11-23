from django.db import transaction
from django.db.models import Count
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.core.permissions import IsUser, IsModerator
from modules.plans.api.filters import PlanFilter
from modules.plans.api.serializers import (
    PlanModeratorDetailsSerializer,
    PlanListSerializer,
    PlanCommentModeratorListSerializer,
    PlanCommentModeratorSerializer,
)
from modules.plans.models import Plan, PlanComment


class PlanModeratorAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.none()
    serializer_class = PlanListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PlanFilter
    pagination_class = LimitOffsetPagination
    permission_classes = [IsModerator]

    def get_queryset(self):
        return Plan.objects.order_by("-publication_date")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlanModeratorDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @action(methods=["get"], detail=True)
    def comments(self, request, pk=None, *args, **kwargs):
        plan: Plan = self.get_object()
        return Response(
            PlanCommentModeratorSerializer(
                plan.comments.all().order_by("-moderated", "-timestamp"), many=True
            ).data,
            status=status.HTTP_200_OK,
        )
