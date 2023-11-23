from rest_framework import viewsets

from modules.api.serializers import BannerSerializer
from modules.core.models import Banner


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
