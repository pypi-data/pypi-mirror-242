from modules.api.serializers.locality import LocalityWithParentSerializer
from modules.map_works.api.serializers import WorksListSerializer, WorksDetailsSerializer


class WorksOperatorLkoListSerializer(WorksListSerializer):
    locality = LocalityWithParentSerializer()


class WorksOperatorLkoDetailSerializer(WorksDetailsSerializer):
    locality = LocalityWithParentSerializer()
