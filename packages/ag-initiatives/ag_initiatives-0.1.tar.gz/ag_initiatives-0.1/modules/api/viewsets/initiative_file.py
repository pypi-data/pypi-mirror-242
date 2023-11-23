from rest_framework import viewsets, permissions, mixins
from rest_framework.viewsets import GenericViewSet

from modules.api.serializers import InitiativeFileSerializer
from modules.core.models import User
from modules.initiatives.models import InitiativeFile, InitiativeFileType


class InitiativeFileAPI(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]
    queryset = InitiativeFile.objects.all()
    serializer_class = InitiativeFileSerializer

    def get_queryset(self):
        user: User = self.request.user
        return InitiativeFile.objects.filter(owner=user)

    def perform_create(self, serializer):
        file = self.request.FILES.get("file")
        type = (
            InitiativeFileType.IMAGE
            if file.content_type in ["image/png", "image/jpeg"]
            else InitiativeFileType.DOCUMENT
        )
        serializer.save(file=file, type=type, name=file.name)
