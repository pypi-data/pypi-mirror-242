from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from modules.api.serializers import LkoLevelSerializer, LkoTypeSerializer
from modules.core.models import LkoLevel, LkoType


class LkoLevelAPI(viewsets.ModelViewSet):
    """ API для уровня ЛКО. """
    queryset = LkoLevel.objects.all()
    serializer_class = LkoLevelSerializer
    permission_classes = (IsAuthenticated,)


class LkoTypeAPI(viewsets.ModelViewSet):
    """ API для типа ЛКО. """
    queryset = LkoType.objects.all()
    serializer_class = LkoTypeSerializer
    permission_classes = (IsAuthenticated,)
