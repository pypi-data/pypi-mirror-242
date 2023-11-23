from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from modules.ecology.api.serializers import GoodsNServicesItemCategorySerializer
from modules.ecology.models import GoodsNServicesItemCategory


class GoodsNServicesItemCategoryAPI(viewsets.ReadOnlyModelViewSet):
    queryset = GoodsNServicesItemCategory.objects.all()
    serializer_class = GoodsNServicesItemCategorySerializer
