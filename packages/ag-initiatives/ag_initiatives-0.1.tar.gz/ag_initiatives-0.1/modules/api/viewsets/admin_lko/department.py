from typing import Optional

import pydantic
from django.http import JsonResponse, HttpResponse
from pydantic import ValidationError
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import viewsets, status
from rest_framework.response import Response
import json

from modules.api.serializers import DepartmentShortSerializer
from modules.api.viewsets.admin_lko.serializers.department import (
    DepartmentCreateSerializer,
    DepartmentsDetailSerializer
)

from modules.api.serializers.department import DepartmentsMainTreeSerializer

from modules.api.viewsets.admin_lko.serializers.department import DepartmentCreateSerializer
from modules.api.viewsets.admin_lko.serializers import DepartmentAllowedFieldsInfoSerializer
from modules.core.dto.department_permissions import DepartmentPermissionsCreateDto
from modules.core.models import User, Department
from modules.core.models.permissions import ModulesPermissions
from modules.core.permissions import IsAdminLKO
from modules.core.services import DepartmentService
from modules.core.services.admin_lko import AdminLkoService
from modules.initiatives.models import InitiativeCategory
from rest_framework.exceptions import ValidationError as v_error


class DepartmentsAdminLkoAPI(viewsets.ViewSet):
    permission_classes = [IsAdminLKO]
    department_service = DepartmentService()

    valid_permissions = [
        ModulesPermissions.MAP_WORKS,
        ModulesPermissions.PLANS,
        ModulesPermissions.VOTING,
        ModulesPermissions.INITIATIVES,
        ModulesPermissions.APPEALS,
        ModulesPermissions.ENCOURAGEMENTS,
        ModulesPermissions.SUGGESTIONS
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_admin_lko_service(self, user: User):
        return AdminLkoService(user)

    def get_serializer_class(self):
        if self.action == "list":
            return DepartmentsMainTreeSerializer
        elif self.action == "retrieve":
            return DepartmentsDetailSerializer
        elif self.action in ["create", "update"]:
            return DepartmentCreateSerializer

    def retrieve(self, request: Request, pk: int):
        admin_lko_service = self.get_admin_lko_service(request.user)

        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentsDetailSerializer(department)

        return Response(serializer.data)

    def list(self, request: Request):
        admin_lko_service = self.get_admin_lko_service(request.user)
        serializer = self.get_serializer_class()(admin_lko_service.get_allowed_departments_tree())
        return Response(serializer.data)

    def create(self, request: Request):
        admin_lko_service = self.get_admin_lko_service(request.user)
        data = json.loads(request.data.get("data"))
        serializer = self.get_serializer_class()(
            data=data,
            context={"image": request.FILES.get("image")}
        )

        permissions_dto: Optional[DepartmentPermissionsCreateDto] = None

        sub_permissions_data = data.pop("sub_permissions") if data.get("sub_permissions") else None

        if sub_permissions_data:
            try:
                pure_categories = sub_permissions_data["initiative_categories"]
                permissions_dto = DepartmentPermissionsCreateDto.parse_obj(sub_permissions_data)
            except pydantic.ValidationError as err:
                return Response(err.errors()[0], status=status.HTTP_400_BAD_REQUEST)

            # TODO Экстра фикс тужен рефактор 16.11
            categories = pure_categories
            subcategories = sub_permissions_data["initiative_subcategories"]

            for category_id in categories:
                if not InitiativeCategory.objects.filter(id=category_id, parent__isnull=True).exists():
                    continue
                category_pk_which_parent_is_curr_category = InitiativeCategory.objects.filter(
                    parent__id=category_id).values_list('id', flat=True)
                if not set(subcategories).intersection(set(category_pk_which_parent_is_curr_category)):
                    raise v_error("Ошибка, необходимо корректно заполнить данные")

        department = admin_lko_service.create_department_with_permissions(serializer, permissions_dto)
        return Response(DepartmentsDetailSerializer(department).data)

    def update(self, request: Request, pk: int):
        admin_lko_service = self.get_admin_lko_service(request.user)
        data = json.loads(request.data.get("data"))

        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer_class()(
            instance=department,
            data=data,
            context={"image": request.FILES.get("image")},
        )

        permissions_dto: Optional[DepartmentPermissionsCreateDto] = None

        sub_permissions_data = data.pop("sub_permissions") if data.get("sub_permissions") else None
        pure_categories = []
        if sub_permissions_data:
            try:
                if ("initiative_categories" in sub_permissions_data and "initiative_subcategories"
                        in sub_permissions_data):
                    pure_categories = sub_permissions_data["initiative_categories"]
                    sub_permissions_data["initiative_categories"] += sub_permissions_data["initiative_subcategories"]
                permissions_dto = DepartmentPermissionsCreateDto.parse_obj(sub_permissions_data)
            except pydantic.ValidationError as err:
                return Response(err.errors()[0], status=status.HTTP_400_BAD_REQUEST)

            # TODO Экстра фикс тужен рефактор 16.11
            categories = pure_categories
            subcategories = sub_permissions_data["initiative_subcategories"]

            for category_id in categories:
                if not InitiativeCategory.objects.filter(id=category_id, parent__isnull=True).exists():
                    continue
                category_pk_which_parent_is_curr_category = InitiativeCategory.objects.filter(
                    parent__id=category_id).values_list('id', flat=True)
                if not set(subcategories).intersection(set(category_pk_which_parent_is_curr_category)):
                    raise v_error("Ошибка, необходимо корректно заполнить данные")

        if permissions_dto is None or not any(permission in self.valid_permissions
                                              for permission in permissions_dto.modules_permissions):
            raise Exception("Должно быть заполнено хотя бы одно поле из прав модулей.")

        department = admin_lko_service.create_department_with_permissions(serializer, permissions_dto)
        return Response(DepartmentsDetailSerializer(department).data)

    @action(detail=True, methods=["get"], url_path="allowed-fields-info")
    def allowed_fields_info(self, request: Request, pk: int):
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response("Огранизация не найдена", status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentAllowedFieldsInfoSerializer(department)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="children")
    def children(self, request: Request, pk: int):
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response("Огранизация не найдена", status=status.HTTP_404_NOT_FOUND)

        children = self.department_service.get_all_departments(department)
        serializer = DepartmentShortSerializer(children, many=True)
        return Response(serializer.data)
