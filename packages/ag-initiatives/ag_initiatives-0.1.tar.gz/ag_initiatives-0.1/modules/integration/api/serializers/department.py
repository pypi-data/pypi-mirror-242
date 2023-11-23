from rest_framework import serializers

from modules.api.serializers import DepartmentShortSerializer
from modules.api.viewsets.admin_lko.serializers.department import DepartmentSubInfoSerializer, \
    DepartmentSubPermissionsSerializer
from modules.core.models import Department


class DepartmentFullSerializer(serializers.ModelSerializer):
    parent = DepartmentShortSerializer(read_only=True)
    sub_info = DepartmentSubInfoSerializer(read_only=True)
    sub_permissions = DepartmentSubPermissionsSerializer(read_only=True)

    class Meta:
        model = Department
        exclude = ['additional_filtering', 'categories']
