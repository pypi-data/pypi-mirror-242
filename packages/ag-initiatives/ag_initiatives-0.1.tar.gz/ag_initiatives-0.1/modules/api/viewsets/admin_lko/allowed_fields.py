from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.viewsets.admin_lko.serializers import DepartmentAllowedFieldsInfoSerializer
from modules.core.models import Department
from modules.core.permissions import IsAdminLKO


class AllowedFieldsAPI(viewsets.ViewSet):

    permission_classes = [IsAdminLKO]

    def list(self, request: Request):
        department = request.GET.get('organization', None)
        if not department:
            serializer = DepartmentAllowedFieldsInfoSerializer(request.user.sub_permissions.admin_lko_permissions.department)
        else:
            department = Department.objects.get(id=department)
            serializer = DepartmentAllowedFieldsInfoSerializer(department)
        return Response(serializer.data)
    