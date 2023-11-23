from rest_framework import mixins
from rest_framework import viewsets

from modules.api.permissions import IsModerator, IsOperator
from modules.api.serializers import InitiativeRejectReasonSerializer
from modules.initiatives.models import InitiativeRejectReason


class InitiativeRejectReasonViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = InitiativeRejectReasonSerializer
    permission_classes = [IsModerator | IsOperator]
    queryset = InitiativeRejectReason.objects.all()
