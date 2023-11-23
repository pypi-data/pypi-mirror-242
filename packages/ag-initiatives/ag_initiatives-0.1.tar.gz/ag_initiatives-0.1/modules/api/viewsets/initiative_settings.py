from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.api.serializers import InitiativeSettingsSerializer
from modules.initiatives.models import InitiativeSettings


class InitiativeSettingsAPI(mixins.ListModelMixin, GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response(InitiativeSettingsSerializer(InitiativeSettings.load()).data)
