from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.api.filters import LocalityFilter
from modules.api.serializers import LocalitySerializer, LocalityTypeSerializer
from modules.core.models import Locality, LocalityType
from modules.core.models.locality import LocalityCategory


class LocalityAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Locality.objects.order_by("order", "name")
    serializer_class = LocalitySerializer
    filterset_class = LocalityFilter
    filter_backends = (filters.DjangoFilterBackend,)

    @action(methods=["get"], detail=False)
    def default(self, request):
        return Response(self.get_serializer(Locality.objects.get(pk=1)).data)


class LocalityTypeAPI(viewsets.ReadOnlyModelViewSet):
    """ API для типов населённых пунктов и МО. """
    queryset = LocalityType.objects.all()
    serializer_class = LocalityTypeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        localities = queryset.filter(category=LocalityCategory.LOCALITY)
        municipalities = queryset.filter(category=LocalityCategory.MUNICIPALITY)

        locality_serializer = self.get_serializer(localities, many=True)
        municipality_serializer = self.get_serializer(municipalities, many=True)

        return Response({
            'localities': locality_serializer.data,
            'municipalities': municipality_serializer.data
        }, status=status.HTTP_200_OK)
