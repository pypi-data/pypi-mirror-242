from django.db.models import Prefetch
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from modules.core.authentication_classes import ExternalSystemTokenAuthentication
from modules.core.models import Locality
from modules.initiatives.models import Initiative
from modules.integration.api.filters.initiative import InitiativeFilter
from modules.integration.api.serializers.initiative import InitiativeIntegrationSerializer
from modules.integration.permissions import CanGetInitiatives


class InitiativeAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InitiativeFilter
    serializer_class = InitiativeIntegrationSerializer
    permission_classes = [CanGetInitiatives]
    authentication_classes = [ExternalSystemTokenAuthentication]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Initiative.objects.select_related(
            "category__parent",
        ).prefetch_related(
            Prefetch(
                "locality",
                queryset=Locality.objects.all().select_related("type"),
            )
        )
