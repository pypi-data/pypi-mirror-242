from rest_framework import viewsets, permissions, mixins
from rest_framework.viewsets import GenericViewSet

from modules.core.models import User
from modules.api.serializers.file import FileSerializer
from modules.core.models import File, FileType


class FileAPI(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        file = self.request.FILES.get("file")
        type = (
            FileType.IMAGE
            if file.content_type in ["image/png", "image/jpeg"]
            else FileType.DOCUMENT
        )
        serializer.save(file=file, type=type, name=file.name)
        return file.name
