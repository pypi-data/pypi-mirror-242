from django.db import transaction
from rest_framework import permissions, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.appeals_pos.models.file import File
from modules.appeals_pos.serializers.file import FileSerializer
from modules.appeals_pos.services.smev.pos_smev_service import PosSmevService


class FileAPI(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = File.objects.all()
    serializer_class = FileSerializer
    pos_service = PosSmevService()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = [{"file": file, "name": file.name} for file in request.FILES.getlist("files")]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)
