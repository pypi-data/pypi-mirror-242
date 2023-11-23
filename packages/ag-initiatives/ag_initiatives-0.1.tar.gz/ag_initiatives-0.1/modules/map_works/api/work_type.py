from rest_framework import viewsets

from modules.map_works.api.serializers import WorkTypeSerializer
from modules.map_works.models import WorkType


class WorkTypeAPI(viewsets.ReadOnlyModelViewSet):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer
