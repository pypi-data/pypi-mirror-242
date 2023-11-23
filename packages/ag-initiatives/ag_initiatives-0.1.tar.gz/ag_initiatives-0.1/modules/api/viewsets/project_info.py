from rest_framework import viewsets

from modules.api.serializers import ProjectInfoSerializer
from modules.core.models import ProjectInfo


class ProjectInfoSerializerAPI(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectInfo.objects.filter(is_project_info=True)
    serializer_class = ProjectInfoSerializer
