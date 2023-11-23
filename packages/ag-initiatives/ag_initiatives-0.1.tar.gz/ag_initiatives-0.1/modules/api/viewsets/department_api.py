from typing import Dict, List

from django.db.models import Q
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from modules.api.filters import CommonDepartmentFilter
from modules.api.serializers import DepartmentShortSerializer, DepartmentStatusSerializer
from modules.api.serializers.user import UserEmployeeSerializer
from modules.core.models import Department, User
from modules.core.permissions import IsOperator, IsAdminLKO
from modules.core.services import DepartmentService


class DepartmentAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentShortSerializer
    permission_classes = [IsOperator]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CommonDepartmentFilter

    department_service = DepartmentService()

    def get_employees(self, department: Department):
        """Получить пользователей, работающих в этой организации"""

        operator_department_filter = \
            Q(sub_permissions__operator_permissions__department__in=
              self.department_service.get_all_departments(department))

        admin_department_filter = \
            Q(sub_permissions__admin_lko_permissions__department__in=
              self.department_service.get_all_departments(department))

        curator_department_filter = \
            Q(sub_permissions__curator_permissions__department__in=
              self.department_service.get_all_departments(department)
              )

        default_department_filter = Q(department__in=self.department_service.get_all_departments(department))

        return User.objects\
            .filter(operator_department_filter
                    | admin_department_filter
                    | curator_department_filter
                    | default_department_filter)\
            .exclude(pk=self.request.user.pk).distinct()

    @action(
        methods=["get"],
        detail=True,
        url_path="employees",
        url_name="employees-retrieve",
        permission_classes=[IsOperator | IsAdminLKO]
    )
    def retrieve_with_employees(self, request, pk=None):
        instance: Department = self.get_object()
        employees = self.get_employees(department=instance)
        return Response(UserEmployeeSerializer(employees, many=True).data)


class DepartmentArchivingAPI(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentStatusSerializer
    permission_classes = [IsOperator]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CommonDepartmentFilter


