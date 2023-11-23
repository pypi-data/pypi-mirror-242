from rest_framework import viewsets

from modules.api.serializers import LkoVotingDescriptionSerializer
from modules.core.models import LkoVotingDescription


class LkoVotingDescriptionAPI(viewsets.ReadOnlyModelViewSet):
    queryset = LkoVotingDescription.objects.all()
    serializer_class = LkoVotingDescriptionSerializer