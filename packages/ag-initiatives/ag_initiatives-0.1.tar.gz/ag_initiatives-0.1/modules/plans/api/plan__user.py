from django.db import transaction
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.core.permissions import IsUser
from modules.plans.api.filters import PlanFilter
from modules.plans.api.serializers import PlanDetailsSerializer, PlanListSerializer
from modules.plans.models import Plan, PlanComment


class PlanUserAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.none()
    serializer_class = PlanListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PlanFilter
    pagination_class = LimitOffsetPagination
    permission_classes = [IsUser]

    def get_queryset(self):
        return Plan.objects.filter(publication_date__lte=timezone.now()).order_by(
            "-publication_date"
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlanDetailsSerializer
        return super().get_serializer_class()

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def comment(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        text = request.data.get("text", None)

        if text is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if len(text) > 500:
            return Response(
                "Слишком длинный комментарий", status=status.HTTP_400_BAD_REQUEST
            )

        PlanComment.objects.create(
            plan=instance,
            text=text,
            timestamp=timezone.now(),
            user=request.user,
        )

        return Response(
            PlanDetailsSerializer(instance).data, status=status.HTTP_201_CREATED
        )
