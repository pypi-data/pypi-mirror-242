from rest_framework import viewsets

from modules.api.serializers import LkoInitiativeDescriptionSerializer
from modules.core.models import LkoInitiativeDescription


class LkoInitiativeDescriptionAPI(viewsets.ReadOnlyModelViewSet):
    queryset = LkoInitiativeDescription.objects.all()
    serializer_class = LkoInitiativeDescriptionSerializer
