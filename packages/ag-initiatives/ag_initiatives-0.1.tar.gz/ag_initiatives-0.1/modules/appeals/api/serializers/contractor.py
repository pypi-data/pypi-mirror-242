from rest_framework import serializers

from modules.appeals.models import Contractor


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = '__all__'
        ref_name = 'appeals_contractor_serializer'
