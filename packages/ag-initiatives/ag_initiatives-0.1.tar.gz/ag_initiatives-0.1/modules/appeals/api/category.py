from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from modules.appeals.api.serializers import (
    CategoryTreeSerializer,
    CategorySerializer,
    CategoryDetailedSerializer,
)
from modules.core.models import User, Locality
from modules.appeals.models import Category, appeal


class CategoryAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        return Response(
            CategoryTreeSerializer(
                Category.objects.filter(parent__isnull=True), many=True
            ).data
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CategoryDetailedSerializer
        return super().get_serializer_class()
