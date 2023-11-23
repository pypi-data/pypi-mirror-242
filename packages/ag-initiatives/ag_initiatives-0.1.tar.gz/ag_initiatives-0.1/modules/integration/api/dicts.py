from django.db.models import Prefetch
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.api.serializers import CategoryCitizenSerializer
from modules.core.authentication_classes import ExternalSystemTokenAuthentication
from modules.core.models import LocalityTypeEnum, Locality, Organization, Category, CategoryCitizen, Department
from modules.ecology.models import UserBalanceOperationType, EventCategory, GoodsNServicesItemCategory
from modules.initiatives.models import InitiativeCategory
from modules.integration.api.serializers.department import DepartmentFullSerializer
from modules.integration.api.serializers.event import EventCategoryIntegrationSerializer
from modules.integration.api.serializers.goodsnservicesitem import GoodsNServicesItemCategoryIntegrationSerializer
from modules.integration.api.serializers.initiative import InitiativeCategoryChildrenSerializer
from modules.integration.api.serializers.voting import LocalityVoteSerializer, CategoryVoteSerializer
from modules.integration.enums.signals_event_type import SignalsEventType
from modules.integration.permissions import CanGetSystemManuals


class DictAPI(GenericAPIView):
    permission_classes = [CanGetSystemManuals]
    authentication_classes = [ExternalSystemTokenAuthentication]

    @staticmethod
    def get(request, *args, **kwargs):
        localities = LocalityVoteSerializer(Locality.objects.select_related("type"), many=True).data
        # TODO Объединение справочников 11.11.2023
        # organizations = OrganizationFullSerializer(Organization.objects.all(), many=True).data
        departments = DepartmentFullSerializer(Department.objects.select_related(
            'parent', 'sub_info', 'sub_permissions'
        ).all(), many=True).data
        voting_categories = CategoryVoteSerializer(Category.objects.prefetch_related("images"), many=True).data
        initiatives_categories_qs = InitiativeCategory.objects.prefetch_related(
            Prefetch(
                "children",
                queryset=InitiativeCategory.objects.prefetch_related("children")
            ),
        )
        initiatives_categories = InitiativeCategoryChildrenSerializer(initiatives_categories_qs, many=True).data
        offers_categories = EventCategoryIntegrationSerializer(EventCategory.objects.all(), many=True).data
        rewards_categories = GoodsNServicesItemCategoryIntegrationSerializer(GoodsNServicesItemCategory.objects.all(), many=True).data
        category_citizen = CategoryCitizenSerializer(CategoryCitizen.objects.all(), many=True).data
        data = {
            "operation_types": [{"id": id, "name": name} for id, name in UserBalanceOperationType.CHOICES],
            "locality_types": [{"id": id, "name": name} for id, name in LocalityTypeEnum.CHOICES],
            "localities": localities,
            # TODO Объединение справочников 11.11.2023
            # "organizations": organizations,
            "departments": departments,
            "voting_categories": voting_categories,
            "initiatives_categories": initiatives_categories,
            "offers_categories": offers_categories,
            "rewards_categories": rewards_categories,
            "category_citizen": category_citizen,
            "signals_event_type": [{"id": id, "name": name} for id, name in SignalsEventType.CHOICES],
        }
        return Response(data)
