from rest_framework import viewsets, permissions, mixins
from rest_framework.viewsets import GenericViewSet

from modules.core.models import User
from modules.appeals.api.serializers.file import FileSerializer
from modules.appeals.models import File, FileType


class FileAPI(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        user: User = self.request.user
        return File.objects.filter(owner=user)

    def perform_create(self, serializer):
        file = self.request.FILES.get("file")
        type = (
            FileType.IMAGE
            if file.content_type in ["image/png", "image/jpeg"]
            else FileType.DOCUMENT
        )
        serializer.save(file=file, type=type, name=file.name)
