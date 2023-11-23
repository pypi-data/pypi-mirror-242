from typing import List, Set

from rest_framework import serializers

from modules.api.serializers import DepartmentShortSerializer, DepartmentStatusSerializer
from modules.core.models import User, SubPermissions, OperatorLkoPermissions, Department, AdminLkoPermissions, UserRole
from modules.core.models.permissions import CuratorPermissions
from modules.core.models.permissions.sub_permissions import LKO_ROLES
from modules.core.services.locality import LocalityService


class OperatorLkoPermissionsSerializer(serializers.ModelSerializer):
    department = DepartmentShortSerializer()

    locality_service = LocalityService()

    voting_localities = serializers.SerializerMethodField()
    initiatives_localities = serializers.SerializerMethodField()
    map_works_localities = serializers.SerializerMethodField()
    plans_localities = serializers.SerializerMethodField()

    class Meta:
        model = OperatorLkoPermissions
        exclude = [
            "voting_municipalities",
            "initiatives_municipalities",
            "map_works_municipalities",
            "plans_municipalities",
            # "is_can_create_subdepartment",
            # "is_can_edit_department",
            # "is_can_edit_subdepartment",
        ]
        read_only_fields = ('is_active',)

    def get_voting_localities(self, instance: OperatorLkoPermissions) -> List[int]:
        # localities = self.locality_service\
        #     .get_all_localities(list(instance.voting_localities.all()) + list(instance.voting_municipalities.all()))
        # return list(map(lambda locality: locality.id, localities))
        return list(instance.voting_localities.all().values_list('id', flat=True))

    def get_initiatives_localities(self, instance: OperatorLkoPermissions) -> List[int]:
        # localities = self.locality_service \
        #     .get_all_localities(list(instance.initiatives_localities.all()) + list(instance.initiatives_municipalities.all()))
        # return list(map(lambda locality: locality.id, localities))
        return list(instance.initiatives_localities.all().values_list('id', flat=True))

    def get_map_works_localities(self, instance: OperatorLkoPermissions) -> List[int]:
        # localities = self.locality_service \
        #     .get_all_localities(list(instance.map_works_localities.all()) + list(instance.map_works_municipalities.all()))
        # return list(map(lambda locality: locality.id, localities))
        return list(instance.map_works_localities.all().values_list('id', flat=True))

    def get_plans_localities(self, instance: OperatorLkoPermissions) -> List[int]:
        # localities = self.locality_service \
        #     .get_all_localities(list(instance.plans_localities.all()) + list(instance.plans_municipalities.all()))
        # return list(map(lambda locality: locality.id, localities))
        return list(instance.plans_localities.all().values_list('id', flat=True))


class AdminLkoPermissionsSerializer(serializers.ModelSerializer):
    department = DepartmentShortSerializer()

    class Meta:
        model = AdminLkoPermissions
        fields = [
            "department",
            'is_active',
            "is_can_create_subdepartment",
            "is_can_edit_department",
            "is_can_edit_subdepartment",
        ]
        read_only_fields = ('is_active',)


class CuratorLkoPermissionsSerializer(serializers.ModelSerializer):
    department = DepartmentShortSerializer()

    locality_service = LocalityService()

    voting_localities = serializers.SerializerMethodField()
    initiatives_localities = serializers.SerializerMethodField()
    map_works_localities = serializers.SerializerMethodField()
    plans_localities = serializers.SerializerMethodField()

    class Meta:
        model = CuratorPermissions
        exclude = [
            "voting_municipalities",
            "initiatives_municipalities",
            "map_works_municipalities",
            "plans_municipalities",
        ]
        read_only_fields = ('is_active',)

    def get_voting_localities(self, instance: CuratorPermissions) -> List[int]:
        localities = self.locality_service\
            .get_all_localities(list(instance.voting_localities.all()) + list(instance.voting_municipalities.all()))
        return list(map(lambda locality: locality.id, localities))

    def get_initiatives_localities(self, instance: CuratorPermissions) -> List[int]:
        localities = self.locality_service \
            .get_all_localities(list(instance.initiatives_localities.all()) + list(instance.initiatives_municipalities.all()))
        return list(map(lambda locality: locality.id, localities))

    def get_map_works_localities(self, instance: CuratorPermissions) -> List[int]:
        localities = self.locality_service \
            .get_all_localities(list(instance.map_works_localities.all()) + list(instance.map_works_municipalities.all()))
        return list(map(lambda locality: locality.id, localities))

    def get_plans_localities(self, instance: CuratorPermissions) -> List[int]:
        localities = self.locality_service \
            .get_all_localities(list(instance.plans_localities.all()) + list(instance.plans_municipalities.all()))
        return list(map(lambda locality: locality.id, localities))


class SubPermissionsSerializer(serializers.ModelSerializer):
    operator_permissions = OperatorLkoPermissionsSerializer()
    admin_lko_permissions = AdminLkoPermissionsSerializer()
    curator_permissions = CuratorLkoPermissionsSerializer(many=True)

    class Meta:
        model = SubPermissions
        fields = "__all__"


class AdminLkoUserShortSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    departments = serializers.SerializerMethodField()
    status = serializers.CharField(source="sub_permissions.status")

    class Meta:
        model = User
        fields = [
            "id",
            "status",
            "username",
            "first_name",
            "last_name",
            "patronymic_name",
            "roles",
            "departments",
            "is_archive",
        ]

    def get_roles(self, user: User):
        roles = set(filter(lambda role: role in LKO_ROLES, user.roles))
        return roles

    def get_departments(self, user: User):
        departments = []
        if hasattr(user.sub_permissions, "operator_permissions"):
            department = user.sub_permissions.operator_permissions.department
            departments.append({
                "id": department.id,
                "name": department.name,
                "image": department.image.url if department.image.name else None,
                "status": department.status,
                "role": UserRole.OPERATOR,
                })
        if hasattr(user.sub_permissions, "admin_lko_permissions"):
            department = user.sub_permissions.admin_lko_permissions.department
            departments.append({
                "id": department.id,
                "name": department.name,
                "image": department.image.url if department.image.name else None,
                "status": department.status,
                "role": UserRole.ADMIN_LKO,
                })
        return departments


class AdminLkoUserDetailSerializer(serializers.ModelSerializer):
    sub_permissions = SubPermissionsSerializer()
    roles = serializers.SerializerMethodField()
    status = serializers.CharField(source="sub_permissions.status")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "patronymic_name",
            "status",
            "roles",
            "phone",
            "work_phone",
            "work_email",
            "sub_permissions",
            "is_archive",
        ]

    def get_roles(self, user: User):
        roles = set(filter(lambda role: role in LKO_ROLES, user.roles))
        return roles


class AdminLkoUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "phone",
            "is_archive",
            "work_phone",
            "work_email",
        ]

