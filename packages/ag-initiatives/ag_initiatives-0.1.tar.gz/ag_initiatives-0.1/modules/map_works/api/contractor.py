from rest_framework import viewsets

from modules.core.permissions import IsOperator
from modules.map_works.api.serializers import ContractorSerializer
from modules.map_works.models import Contractor


class ContractorAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = [IsOperator]
