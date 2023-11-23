from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from modules.api.serializers.category_citizen import CategoryCitizenSerializer

from modules.core.authentication_classes import ExternalSystemTokenAuthentication
from modules.integration.permissions import CanTransmitCitizenCategories


class CitizenCategoryApi(CreateModelMixin, GenericViewSet):
    """API for check access to system for specific token, which hand out for external systems."""

    authentication_classes = (ExternalSystemTokenAuthentication,)
    serializer_class = CategoryCitizenSerializer
    permission_classes = (CanTransmitCitizenCategories,)
