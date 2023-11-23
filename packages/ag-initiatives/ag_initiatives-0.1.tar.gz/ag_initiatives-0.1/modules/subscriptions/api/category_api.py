from typing import List
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from modules.subscriptions.api.serializers import CategorySerializer


class CategoryAPI(viewsets.ViewSet):
    """Категории отслеживаемых модулей"""

    permission_classes: List = [permissions.IsAuthenticated]
    http_method_names: List[str] = ["get"]
    serializer_class = CategorySerializer

    def list(self, request):
        data: List = self.serializer_class.data()
        response = Response(data, status=status.HTTP_200_OK)
        return response
