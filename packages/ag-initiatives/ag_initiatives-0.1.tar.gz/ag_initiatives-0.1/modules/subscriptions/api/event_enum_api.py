from typing import List

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from modules.subscriptions.enums import EventEnum


class EventEnumAPI(viewsets.ViewSet):
    """События"""

    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

    def list(self, request):
        data: List = EventEnum.__json__()
        response = Response(data, status=status.HTTP_200_OK)
        return response
