from django.db import transaction
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.core.permissions import IsUser, IsModerator
from modules.plans.api.filters import PlanFilter
from modules.plans.api.serializers import (
    PlanCommentModeratorListSerializer,
    PlanCommentModeratorSerializer,
    PlanCommentModeratorListSerializer2,
)
from modules.plans.models import PlanComment


class PlanCommentModeratorAPI(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = PlanComment.objects.none()
    serializer_class = PlanCommentModeratorListSerializer2
    pagination_class = LimitOffsetPagination
    permission_classes = [IsModerator]

    def get_queryset(self):
        if self.action == "destroy":
            return PlanComment.objects.all()
        return PlanComment.objects.all().order_by("-moderated", "-timestamp")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlanCommentModeratorListSerializer2
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    def list(self, request, *args, **kwargs):
        # todo: сделай группировку
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    @action(methods=["get"], detail=True)
    def accept(self, request, pk=None, *args, **kwargs):
        instance: PlanComment = self.get_object()

        if instance.moderated is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        instance.moderated = True
        instance.save(update_fields=["moderated"])

        return Response(status=status.HTTP_200_OK)
