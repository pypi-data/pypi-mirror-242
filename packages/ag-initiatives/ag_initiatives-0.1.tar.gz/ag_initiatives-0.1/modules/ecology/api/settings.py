from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from modules.ecology.api.serializers import SettingsSerializer
from modules.ecology.models import Settings


class SettingsAPI(viewsets.ViewSet):

    permission_classes = [AllowAny]

    def list(self, request):
        settings = Settings.load()
        return Response(SettingsSerializer(settings).data)

    @action(methods=["get"], detail=False, url_path="status-instruction")
    def status_instruction(self, request):
        settings = Settings.objects.first()
        return Response(settings.status_instruction)

    @action(methods=["get"], detail=False, url_path="module-information")
    def module_information(self, request):
        settings = Settings.objects.first()
        return Response(settings.module_information)
