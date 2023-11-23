from rest_framework import viewsets

from modules.map_works.api.serializers import WorkReasonSerializer
from modules.map_works.models import WorkReason


class WorkReasonAPI(viewsets.ReadOnlyModelViewSet):
    queryset = WorkReason.objects.all()
    serializer_class = WorkReasonSerializer
