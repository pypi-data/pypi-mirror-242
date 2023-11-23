from rest_framework import viewsets
from rest_framework.response import Response

from modules.plans.api.serializers import (
    CategoryTreeSerializer,
    CategorySerializer,
    CategoryDetailedSerializer,
)
from modules.plans.models import Category


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
