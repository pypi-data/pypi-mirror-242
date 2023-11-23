from typing import List

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from modules.subscriptions.enums import ActiveCitizenModuleEnum


class ActiveCitizenModuleEnumAPI(viewsets.ViewSet):
    """Перечень отслеживаемых модулей проекта"""

    permission_classes: List = [permissions.IsAuthenticated]
    http_method_names: List[str] = ["get"]

    def list(self, request):
        data = ActiveCitizenModuleEnum.__json__()
        response = Response(data, status=status.HTTP_200_OK)
        return response
