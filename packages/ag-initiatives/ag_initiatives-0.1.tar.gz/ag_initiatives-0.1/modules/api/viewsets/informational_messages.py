from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from modules.api.serializers import InformationalMessagesSerializer
from modules.core.models import InformationalMessages


class InformationalMessagesAPI(viewsets.ModelViewSet):
    """ API для информационных сообщений. """
    queryset = InformationalMessages.objects.all()
    serializer_class = InformationalMessagesSerializer
