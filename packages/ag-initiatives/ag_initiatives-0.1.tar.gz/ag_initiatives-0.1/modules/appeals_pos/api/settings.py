from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from modules.appeals_pos.models import Settings
from modules.appeals_pos.serializers import SettingsSerializer


class SettingsApi(viewsets.ViewSet):

    serializer_class = SettingsSerializer

    def list(self, request: Request):
        settings = Settings.load()
        return Response(self.serializer_class(settings).data)
