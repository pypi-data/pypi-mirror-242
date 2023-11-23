from rest_framework import viewsets

from modules.api.serializers import MainPageBlockSerializer
from modules.core.models import MainPageBlock


class MainPageBlockAPI(viewsets.ReadOnlyModelViewSet):
    queryset = MainPageBlock.objects.all()
    serializer_class = MainPageBlockSerializer
