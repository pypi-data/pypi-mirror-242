from rest_framework import viewsets

from modules.map_works.api.serializers import InstitutionTypeSerializer
from modules.map_works.models import InstitutionType


class InstitutionTypeAPI(viewsets.ReadOnlyModelViewSet):
    queryset = InstitutionType.objects.all()
    serializer_class = InstitutionTypeSerializer
