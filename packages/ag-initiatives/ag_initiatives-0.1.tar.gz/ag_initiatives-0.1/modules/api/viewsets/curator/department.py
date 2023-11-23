from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from django.db.models import Q

from modules.api.filters import DepartmentFilter
from modules.api.pagination import DefaultPagination
from modules.api.serializers import DepartmentTreeSerializer
from modules.api.viewsets.admin_lko.serializers.department import DepartmentsDetailSerializer
from modules.api.viewsets.curator.serializers import DepartmentAllowedFieldsInfoSerializer
from modules.core.models import Department
from modules.core.permissions import IsOperator
from modules.core.services import DepartmentService


class DepartmentsCuratorAPI(viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsOperator]
    filterset_class = DepartmentFilter
    department_service = DepartmentService()

    def get_queryset(self):
        curator_permissions = self.request.user.sub_permissions.curator_permissions.all()
        curator_departments = set(map(lambda permissions: permissions.department, curator_permissions))
        curator_departments_ids = set(map(lambda permissions: permissions.department.pk, curator_permissions))

        if self.action == "list":
            return Department.objects.filter(pk__in=curator_departments_ids)

        elif self.action in ["retrieve", "count"]:
            all_departments = set()
            for department in curator_departments:
                inner_departments = set(self.department_service.get_all_departments_generator(department))
                all_departments.update(inner_departments)

            all_departments_ids = list(map(lambda department: department.pk, all_departments))
            return Department.objects.filter(pk__in=all_departments_ids)

    def get_serializer_class(self):
        if self.action == "list":
            return DepartmentTreeSerializer
        elif self.action == "retrieve":
            return DepartmentsDetailSerializer

    @action(detail=True, methods=["get"], url_path="allowed-fields-info")
    def allowed_fields_info(self, request: Request, pk: int):
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response("Огранизация не найдена", status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentAllowedFieldsInfoSerializer(department)
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def count(self, request: Request) -> Response:
        return Response({
            "count": self.filter_queryset(self.get_queryset()).count()
        })
