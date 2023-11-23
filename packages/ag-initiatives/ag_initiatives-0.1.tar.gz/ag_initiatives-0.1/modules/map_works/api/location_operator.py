from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from modules.core.models import User
from modules.core.permissions import IsOperator
from modules.map_works.api.serializers import LocationSerializer
from modules.map_works.models import Location


class LocationOperatorAPI(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Location.objects.none()
    serializer_class = LocationSerializer
    permission_classes = [IsOperator]

    def get_queryset(self):
        user: User = self.request.user

        if not user.department:
            return Location.objects.none()

        return Location.objects.filter(work__owner=user.department)
