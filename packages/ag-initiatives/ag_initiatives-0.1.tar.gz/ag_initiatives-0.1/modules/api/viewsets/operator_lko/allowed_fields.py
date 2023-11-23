from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.serializers import DepartmentShortSerializer
from modules.core.permissions import IsOperator
from modules.core.services import DepartmentService


class AllowedFieldsAPI(viewsets.ViewSet):

    permission_classes = [IsOperator]
    department_service = DepartmentService()

    def list(self, request: Request):
        allowed_departments = self.department_service\
            .get_all_departments(request.user.sub_permissions.operator_permissions.department)

        return Response({
            "allowed_departments": DepartmentShortSerializer(allowed_departments, many=True).data
        })
