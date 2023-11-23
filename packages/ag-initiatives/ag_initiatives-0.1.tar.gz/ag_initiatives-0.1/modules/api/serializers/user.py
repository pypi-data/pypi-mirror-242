from typing import List

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from modules import ecology
from modules.api.serializers import LocalityShortSerializer, DepartmentShortSerializer
from modules.core.models import SubPermissions, UserRole, AdminLkoPermissions, OperatorLkoPermissions, \
    ActiveCitizenModule
from modules.core.models import User
from modules.core.models.active_citizen_module import ActiveCitizenModuleEnum
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
        ]
        read_only_fields = ('is_active',)

    def get_voting_localities(self, instance: OperatorLkoPermissions) -> List[int]:
        localities = self.locality_service \
            .get_all_localities(list(instance.voting_localities.all()) + list(instance.voting_municipalities.all()))
        return list(map(lambda locality: locality.id, localities))

    def get_initiatives_localities(self, instance: OperatorLkoPermissions) -> List[int]:
        localities = self.locality_service \
            .get_all_localities(
            list(instance.initiatives_localities.all()) + list(instance.initiatives_municipalities.all()))
        return list(map(lambda locality: locality.id, localities))

    def get_map_works_localities(self, instance: OperatorLkoPermissions) -> List[int]:
        localities = self.locality_service \
            .get_all_localities(
            list(instance.map_works_localities.all()) + list(instance.map_works_municipalities.all()))
        return list(map(lambda locality: locality.id, localities))

    def get_plans_localities(self, instance: OperatorLkoPermissions) -> List[int]:
        localities = self.locality_service \
            .get_all_localities(list(instance.plans_localities.all()) + list(instance.plans_municipalities.all()))
        return list(map(lambda locality: locality.id, localities))


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


class SubPermissionsSerializer(serializers.ModelSerializer):
    admin_lko_permissions = AdminLkoPermissionsSerializer()
    operator_permissions = OperatorLkoPermissionsSerializer()

    class Meta:
        model = SubPermissions
        fields = "__all__"


class UserShortSerializer(serializers.ModelSerializer):
    residential_locality = LocalityShortSerializer()
    registration_locality = LocalityShortSerializer()
    department = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    ecology_state = serializers.CharField(source="ecology.state")
    ecology_balance = serializers.IntegerField(source="ecology.balance")
    ecology_status = serializers.SerializerMethodField(method_name="get_ecology_status")
    ecology_earned_bonuses = serializers.IntegerField(source="ecology.earned_bonuses")
    categories = serializers.StringRelatedField(many=True, read_only=True)
    esia_id = serializers.SerializerMethodField()

    sub_permissions = SubPermissionsSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "patronymic_name",
            'esia_id',
            "age",
            "email",
            "work_email",
            "email_initiative_notification",
            "email_appeals_notification",
            "phone",
            "work_phone",
            "roles",
            "residential_locality",
            "registration_locality",
            "esia_verified",
            "department",
            "categories",
            "ecology_state",
            "ecology_status",
            "ecology_balance",
            "ecology_earned_bonuses",
            "is_archive",
            "sub_permissions",
            "last_login",
            "date_joined",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        ecology_stimulation_module = ActiveCitizenModule.objects.filter(
            name=ActiveCitizenModuleEnum.ECOLOGY_STIMULATION).first()
        ecology_offers_module = ActiveCitizenModule.objects.filter(name=ActiveCitizenModuleEnum.ECOLOGY_OFFERS).first()

        if (ecology_stimulation_module and not ecology_stimulation_module.is_worked
                and ecology_offers_module and ecology_offers_module.is_worked):
            to_exclude = [
                "ecology_state",
                "ecology_balance",
                "ecology_status",
                "ecology_earned_bonuses",
            ]
            for field in to_exclude:
                data.pop(field, None)

        return data

    def get_esia_id(self, instance: User):
        esia_id = None
        if hasattr(instance, "esia_id"):
            esia_id = instance.esia_id.split('esia_')
            esia_id = esia_id[1] if len(esia_id) == 2 else None
        return esia_id

    def get_ecology_status(self, instance: User):
        return ecology.services.get_ecology_status(user_profile=instance.ecology)

    def get_department(self, obj):
        department = getattr(obj, "department", None)
        if department:
            return DepartmentShortSerializer(department).data
        return None

    def get_roles(self, obj: User):
        if obj.is_archive:
            return [i for i in obj.roles if i not in [UserRole.ADMIN_LKO, UserRole.OPERATOR, UserRole.MODERATOR]]
        return obj.roles

    @staticmethod
    def get_email(obj: User):
        emails = {
            'user_email': obj.email,
            'user_work_email': obj.work_email,
        }

        try:
            if obj.department:
                user_department_email = getattr(obj.department, "email", None)
                if user_department_email is not None:
                    emails['user_department_email'] = user_department_email
        except ObjectDoesNotExist:
            pass

        try:
            if obj.is_operator:
                operator_department_email = getattr(obj.sub_permissions.operator_permissions.department, "email", None)
                if operator_department_email is not None:
                    emails['operator_department_email'] = operator_department_email
        except ObjectDoesNotExist:
            pass

        try:
            if obj.is_admin_lko:
                admin_lko_department_email = getattr(obj.sub_permissions.admin_lko_permissions.department, "email", None)
                if admin_lko_department_email is not None:
                    emails['admin_lko_department_email'] = admin_lko_department_email
        except ObjectDoesNotExist:
            pass

        return emails


class UserEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "patronymic_name",
            "email",
            "work_email",
            "phone",
        ]


class UploadingUsersSerializer(serializers.ModelSerializer):
    sub_permissions = UserEmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = SubPermissions
        fields = [
            "id",
            "sub_permissions",
            "email",
            "sub_phone",
            "position",
        ]


class UserArchivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "patronymic_name",
            "email",
            "work_email",
            "phone",
            "is_archive",
        ]
