import pydantic
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.viewsets.admin_lko.serializers.user import AdminLkoUserShortSerializer, AdminLkoUserDetailSerializer, \
    AdminLkoUserUpdateSerializer
from modules.api.viewsets.filters import UserFilter
from modules.core.dto.permissions import AdminLkoPermissionsCreateDto, UserSubPermissionsCreateDto
from modules.core.models import User, SubPermissions
from modules.core.permissions import IsAdminLKO
from modules.core.services import AdminLkoService
from modules.initiatives.models import InitiativeCategory
from .mail_invite import MailInviteAPI
from .serializers import DepartmentAllowedFieldsInfoSerializer
from ...pagination import DefaultPagination


class UserManagerApi(viewsets.ViewSet):
    permission_classes = [IsAdminLKO]
    filter_class = UserFilter

    def __init__(self, *args, **kwargs):
        super(UserManagerApi, self).__init__(*args, **kwargs)
        self.paginator = DefaultPagination()

    def get_admin_lko_service(self, user: User):
        return AdminLkoService(user)

    def get_serializer_class(self):
        if self.action == "list":
            return AdminLkoUserShortSerializer
        elif self.action == "retrieve":
            return AdminLkoUserDetailSerializer
        elif self.action == "update":
            return AdminLkoUserUpdateSerializer

    def list(self, request: Request):
        admin_lko_service = self.get_admin_lko_service(request.user)
        users = admin_lko_service.get_allowed_users()

        order_by_param = self.request.query_params.get("order_by", None)

        if order_by_param is not None:
            users = users.order_by(order_by_param)

        filtered_users = self.filter_class(
            data=request.query_params, queryset=users
        ).qs

        paginated_users = self.paginator.paginate_queryset(filtered_users, request)
        serializer = self.get_serializer_class()(paginated_users, many=True)
        response = self.paginator.get_paginated_response(serializer.data)
        return response

    def retrieve(self, request: Request, pk: int):
        admin_lko_service = self.get_admin_lko_service(request.user)
        try:
            user = admin_lko_service.get_allowed_users().get(pk=pk)
        except User.DoesNotExist:
            return Response("Пользователь не найден", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer_class()(user)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="allowed-fields-info")
    def allowed_departments_list(self, request: Request):
        serializer = DepartmentAllowedFieldsInfoSerializer(request.user.department)
        return Response(serializer.data)

    @staticmethod
    def update_user_data(user, sub_permission_dto):
        user.work_email = sub_permission_dto.email
        user.roles = sub_permission_dto.roles
        user.position = sub_permission_dto.position
        user.sub_phone = sub_permission_dto.sub_phone
        user.save()

    @transaction.atomic
    def update(self, request: Request, pk: int):

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        sub_permission_data = request.data.pop("sub_permissions") if request.data.get("sub_permissions") else None
        serializer = self.get_serializer_class()(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        admin_lko_service = self.get_admin_lko_service(request.user)

        if sub_permission_data:
            try:
                sub_permission_dto = UserSubPermissionsCreateDto.parse_obj(sub_permission_data)
            except pydantic.ValidationError as err:
                return Response(err.json(), status=status.HTTP_400_BAD_REQUEST)

            # TODO Экстра фикс тужен рефактор 16.11
            categories = sub_permission_dto.operator_permissions.initiative_categories
            subcategories = sub_permission_dto.operator_permissions.initiative_subcategories

            for category_id in categories:
                category_pk_which_parent_is_curr_category = InitiativeCategory.objects.filter(
                    parent__id=category_id).values_list('id', flat=True)
                if not set(subcategories).intersection(set(category_pk_which_parent_is_curr_category)):
                    raise ValidationError("Ошибка, необходимо корректно заполнить данные")

            self.update_user_data(user, sub_permission_dto)
            sub_permissions = user.sub_permissions if hasattr(user, "sub_permissions") else None
            admin_lko_service.create_or_update_sub_permissions(sub_permission_dto, sub_permissions=sub_permissions,
                                                               user=user)

        return Response(AdminLkoUserDetailSerializer(user).data)

    @action(detail=False, methods=["get"], url_path="allowed-fields-info")
    def allowed_departments_list(self, request: Request):
        serializer = DepartmentAllowedFieldsInfoSerializer(request.user.department)
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=False, methods=['post'], url_path='user-invite')
    def send_user_invite(self, request: Request):
        """Сохраняет информацию(Права, фио, роль...) и отправляет инвайт на почту из запроса"""

        try:
            sub_permission_dto = UserSubPermissionsCreateDto.parse_obj(request.data.get("sub_permissions"))
        except pydantic.ValidationError as err:
            return Response(err.json(), status=status.HTTP_400_BAD_REQUEST)

        admin_lko_service = self.get_admin_lko_service(request.user)
        sub_permissions = SubPermissions.objects.create(email=sub_permission_dto.email)

        admin_lko_service.create_or_update_sub_permissions(
            dto=sub_permission_dto,
            sub_permissions=sub_permissions
        )

        MailInviteAPI().save_data_and_send_mail(request, sub_permissions.pk)

        return Response("Приглашение отправлено.")

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path="update-user-permissions")
    def update_user_permissions(self, request: Request, pk: int):
        """Обновляет (полностью перезаписывает) права на все ЛКО роли пользователя"""

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("Пользователь не найден")

        try:
            sub_permission_dto = UserSubPermissionsCreateDto.parse_obj(request.data)
        except pydantic.ValidationError as err:
            return Response(err.json(), status=status.HTTP_400_BAD_REQUEST)

        admin_lko_service = self.get_admin_lko_service(request.user)
        sub_permissions = user.sub_permissions if hasattr(user, "sub_permissions") else None
        if not sub_permissions:
            sub_permissions = SubPermissions.objects.create(user=user)

        admin_lko_service.update_user_lko_roles(user, sub_permission_dto.roles)
        admin_lko_service.create_or_update_sub_permissions(sub_permission_dto, sub_permissions=sub_permissions,
                                                           user=user)
        return Response()

    def update_admin_lko_permissions(self, request: Request, pk: int):
        try:
            dto = AdminLkoPermissionsCreateDto.parse_obj(request.data)
        except pydantic.ValidationError as err:
            return Response(err.json(), status=status.HTTP_400_BAD_REQUEST)
