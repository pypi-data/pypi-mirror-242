from rest_framework import serializers

from modules.core.models import Department


class DepartmentAsOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'id',
            'name'
        )
