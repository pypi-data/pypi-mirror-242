from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.core.models import Settings


class SettingsApi(viewsets.ViewSet):
    def list(self, request):
        pass

    @action(methods=["get"], detail=False, url_path="privacy-policy")
    def privacy_policy(self, request):
        settings = Settings.load()
        return Response({"data": settings.privacy_policy})
