from rest_framework import viewsets

from modules.map_works.api.serializers import WorkCategorySerializer
from modules.map_works.models import WorkCategory


class WorkCategoryAPI(viewsets.ReadOnlyModelViewSet):
    queryset = WorkCategory.objects.all()
    serializer_class = WorkCategorySerializer
