from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from modules.api.permissions import IsOperator
from modules.api.serializers import (
    InitiativeAcceptingSettingsSerializer,
    InitiativeAcceptingSettingsWriteSerializer,
)
from modules.initiatives.models import InitiativeAcceptingSettings


class InitiativeAcceptingSettingsViewSet(ModelViewSet):
    queryset = InitiativeAcceptingSettings.objects.select_related(
        "department", "category"
    ).prefetch_related('locality')
    permission_classes = (IsOperator,)
    serializer_class = InitiativeAcceptingSettingsSerializer

    def get_queryset(self):
        return self.queryset.filter(
            department=getattr(self.request.user, "department", None)
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return super(
                InitiativeAcceptingSettingsViewSet, self
            ).get_serializer_class()
        return InitiativeAcceptingSettingsWriteSerializer

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({
            "count": self.filter_queryset(self.get_queryset()).count()
        })
