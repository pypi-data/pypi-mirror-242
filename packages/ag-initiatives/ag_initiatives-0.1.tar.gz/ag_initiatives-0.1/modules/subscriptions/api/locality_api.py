from typing import List

from django.db.models import QuerySet
from rest_framework import viewsets, permissions

from modules.api.serializers import LocalitySerializer
from modules.core.models import Locality


class LocalityAPI(viewsets.ModelViewSet):
    """Населенный пункт"""

    queryset: QuerySet = Locality.objects.all()
    permission_classes: List = [permissions.IsAuthenticated]
    serializer_class: LocalitySerializer = LocalitySerializer
    http_method_names: List[str] = ["get"]
