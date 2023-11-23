from modules.api.serializers.locality import LocalityWithParentSerializer
from modules.plans.api.serializers import PlanListSerializer


class PlanOperatorLkoListSerializer(PlanListSerializer):
    locality = LocalityWithParentSerializer()
