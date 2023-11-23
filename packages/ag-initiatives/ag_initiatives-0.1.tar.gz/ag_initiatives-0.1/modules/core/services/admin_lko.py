import random
from typing import Union, Iterable, Set, Optional, List

from django.db import transaction
from django.db.models import QuerySet, Q
from rest_framework.exceptions import ValidationError

# from modules.api.viewsets.admin_lko.serializers.department import DepartmentCreateSerializer
from modules.core.dto.department_permissions import DepartmentPermissionsCreateDto
from modules.core.dto.permissions import (
    OperatorPermissionsCreateDto,
    AdminLkoPermissionsCreateDto,
    UserSubPermissionsCreateDto, CuratorPermissionsCreateDto,
)
from modules.core.exceptions import LkoPermissionError
from modules.core.models import User, Locality, Department, Municipality, InhabitedLocality
from modules.core.models.permissions import DepartmentSubPermissions, CuratorPermissions, ModulesPermissions
from modules.core.models.permissions import SubPermissions, AdminLkoPermissions, OperatorLkoPermissions
from modules.core.models.permissions.sub_permissions import LKO_ROLES
from modules.core.services import DepartmentService
from modules.core.services.department import DepartmentPermissionsServiceFactory
from modules.core.services.locality import LocalityService

from modules.core.models import Category as CoreCategory
from modules.ecology.models import GoodsNServicesItemCategory, EventCategory
from modules.feedback.models import Problematic
from modules.initiatives.models import InitiativeCategory
from modules.map_works.models import WorkCategory
from modules.plans.models import Category as PlanCategory


class AdminLkoService:
    """Сервис, предоставляющий интерфейс от пользователя с ролью Админ ЛКО"""

    def __init__(self,
                 user: User,
                 department_service: DepartmentService = DepartmentService(),
                 locality_service: LocalityService = LocalityService(),
                 department_permissions_service_factory: DepartmentPermissionsServiceFactory
                 = DepartmentPermissionsServiceFactory()
                 ):
        self.user = user
        self.create_default_permissions()
        self._check_default_permissions()
        self.permissions = self.user.sub_permissions.admin_lko_permissions
        self.department_service = department_service
        self.locality_service = locality_service
        self.department_permissions_service_factory = department_permissions_service_factory

    def _get_role_department_localities(self, permissions: Union[OperatorLkoPermissions, CuratorPermissions]) -> \
    Iterable[Locality]:
        return self.locality_service.filter_localities(permissions.department.locality.all())

    def _get_role_department_municipalities(self, permissions: Union[OperatorLkoPermissions, CuratorPermissions]) -> \
    Iterable[Locality]:
        return self.locality_service.filter_municipalities(permissions.department.locality.all())

    @property
    def department(self):
        return self.permissions.department

    def create_default_permissions(self):
        sub_permissions = self.user.sub_permissions if hasattr(self.user, 'sub_permissions') else None
        if not sub_permissions:
            sub_permissions = SubPermissions.objects.create(user=self.user)

        if not hasattr(sub_permissions, 'admin_lko_permissions'):
            if hasattr(self.user, 'admin_lko_permissions') and (
            admin_lko_permissions := self.user.admin_lko_permissions):
                admin_lko_permissions.user = self.user
                admin_lko_permissions.save()
                sub_permissions.admin_lko_permissions = admin_lko_permissions
                sub_permissions.save()
            else:
                AdminLkoPermissions.objects.create(
                    sub_permissions=sub_permissions,
                    department=self.user.department,
                    user=self.user
                )

    def _check_default_permissions(self):
        if not self.user.is_admin_lko:
            raise LkoPermissionError('user doesnt have role admin lko')
        if not self.user.sub_permissions or not self.user.sub_permissions.admin_lko_permissions:
            raise LkoPermissionError('user doesnt have sub permissions')

    def get_allowed_departments_tree(self):
        """Получить организацию пользователя"""
        return self.permissions.department

    def get_allowed_departments(self) -> Iterable[Department]:
        """Получить доступные организации, в которых у этого пользователя есть власть :)"""
        return self.department_service.get_all_departments(self.permissions.department)

    def get_allowed_municipalities_tree(self) -> Union[QuerySet, Locality]:
        return self.permissions.department.locality

    def get_allowed_municipalities_generator(self) -> Iterable[Locality]:
        return self.locality_service.get_all_localities_generator(self.permissions.department.locality)

    def get_allowed_municipalities(self) -> Set[Locality]:
        """Получить доступные муниципальные организации и населенные пункты"""
        return set(self.locality_service.get_all_localities(self.permissions.department.locality))

    def update_user_lko_roles(self, user: User, lko_roles: List[str]):
        """Обновляет роли пользователя, которые относятся к доработкам по ЛКО, остальные не трогает"""
        # not_lko_roles = list(filter(lambda role: role not in LKO_ROLES, user.roles))
        new_roles = lko_roles
        user.roles = new_roles
        user.save(update_fields=["roles"])

    def update_user_lko_roles_when_archiving(self, user: User):
        """
        Удаляет роли пользователя при его архивировании,
        которые относятся к доработкам по ЛКО, остальные не трогает
        """
        not_lko_roles = list(filter(lambda role: role not in LKO_ROLES, user.roles))
        user.roles = not_lko_roles
        user.save(update_fields=["roles"])

    @transaction.atomic
    def create_or_update_admin_lko_permissions(
            self, sub_permissions: SubPermissions, dto: AdminLkoPermissionsCreateDto
    ) -> AdminLkoPermissions:

        """Создает из ДТО права для Администратора ЛКО на указанный объект дополнительных прав пользователя"""

        try:
            department = Department.objects.get(pk=dto.department_id)
        except Department.DoesNotExist:
            raise ValidationError("Такой организации не существует")

        admin_lko_permissions = sub_permissions.admin_lko_permissions \
            if hasattr(sub_permissions, "admin_lko_permissions") else None

        if department not in self.get_allowed_departments():
            raise ValidationError("У вас нет прав создания администратора ЛКО в этой организации")

        if not admin_lko_permissions:
            admin_lko_permissions = AdminLkoPermissions.objects.create(
                sub_permissions=sub_permissions,
                department=department,
                user=sub_permissions.user
            )
        else:
            admin_lko_permissions.department = department
            admin_lko_permissions.user = sub_permissions.user
            admin_lko_permissions.save()
        return admin_lko_permissions

    def set_modules_permissions(
            self,
            permissions: Union[CuratorPermissions, OperatorLkoPermissions],
            dto: Union[CuratorPermissionsCreateDto, OperatorPermissionsCreateDto]
    ) -> Union[CuratorPermissions, OperatorLkoPermissions]:

        """Задает переданному объекту прав права на модули в соответсвии с переданных ДТО"""

        department_voting_permissions_service = self.department_permissions_service_factory.create(
            ModulesPermissions.VOTING,
            self.department
        )
        department_initiative_permissions_service = self.department_permissions_service_factory.create(
            ModulesPermissions.INITIATIVES,
            self.department
        )
        department_plans_permissions_service = self.department_permissions_service_factory.create(
            ModulesPermissions.PLANS,
            self.department
        )
        department_map_works_permissions_service = self.department_permissions_service_factory.create(
            ModulesPermissions.MAP_WORKS,
            self.department
        )
        voting_categories = CoreCategory.objects.filter(pk__in=dto.voting_permissions.allowed_categories_ids) \
            .all() if dto.voting_permissions else []

        voting_municipalities = Municipality.objects.filter(pk__in=dto.voting_permissions.allowed_localities_ids) \
            .all() if dto.voting_permissions and dto.voting_permissions.allowed_localities_ids \
            else self._get_role_department_municipalities(permissions)

        voting_localities = InhabitedLocality.objects.filter(pk__in=dto.voting_permissions.allowed_localities_ids) \
            .all() if dto.voting_permissions and dto.voting_permissions.allowed_localities_ids \
            else self._get_role_department_localities(permissions)

        initiatives_categories = InitiativeCategory.objects.filter(
            pk__in=dto.initiative_permissions.allowed_categories_ids) \
            .all() if dto.initiative_permissions else department_initiative_permissions_service.get_allowed_categories()

        initiatives_municipalities = Municipality.objects.filter(
            pk__in=dto.initiative_permissions.allowed_localities_ids) \
            .all() if dto.initiative_permissions and dto.initiative_permissions.allowed_localities_ids \
            else self._get_role_department_municipalities(permissions)

        initiatives_localities = InhabitedLocality.objects.filter(
            pk__in=dto.initiative_permissions.allowed_localities_ids) \
            .all() if dto.initiative_permissions and dto.initiative_permissions.allowed_localities_ids \
            else self._get_role_department_localities(permissions)

        map_works_categories = WorkCategory.objects.filter(pk__in=dto.map_works_permissions.allowed_categories_ids) \
            .all() if dto.map_works_permissions else department_map_works_permissions_service.get_allowed_categories()

        map_works_municipalities = Municipality.objects.filter(
            pk__in=dto.map_works_permissions.allowed_localities_ids) \
            .all() if dto.map_works_permissions and dto.map_works_permissions.allowed_localities_ids \
            else self._get_role_department_municipalities(permissions)

        map_works_localities = InhabitedLocality.objects.filter(
            pk__in=dto.map_works_permissions.allowed_localities_ids) \
            .all() if dto.map_works_permissions and dto.map_works_permissions.allowed_localities_ids \
            else self._get_role_department_localities(permissions)

        plans_categories = PlanCategory.objects.filter(pk__in=dto.plans_permissions.allowed_categories_ids) \
            .all() if dto.plans_permissions \
            else department_plans_permissions_service.get_allowed_categories()

        plans_municipalities = Municipality.objects.filter(pk__in=dto.plans_permissions.allowed_localities_ids) \
            .all() if dto.plans_permissions and dto.plans_permissions.allowed_localities_ids \
            else self._get_role_department_municipalities(permissions)

        plans_localities = InhabitedLocality.objects.filter(pk__in=dto.plans_permissions.allowed_localities_ids) \
            .all() if dto.plans_permissions and dto.plans_permissions.allowed_localities_ids \
            else self._get_role_department_localities(permissions)

        permissions.voting_categories.set(voting_categories)
        permissions.voting_municipalities.set(voting_municipalities)
        permissions.voting_localities.set(voting_localities)

        permissions.initiatives_categories.set(initiatives_categories)
        permissions.initiatives_municipalities.set(initiatives_municipalities)
        permissions.initiatives_localities.set(initiatives_localities)

        permissions.map_works_categories.set(map_works_categories)
        permissions.map_works_municipalities.set(map_works_municipalities)
        permissions.map_works_localities.set(map_works_localities)

        permissions.plans_categories.set(plans_categories)
        permissions.plans_municipalities.set(plans_municipalities)
        permissions.plans_localities.set(plans_localities)

        return permissions

    @transaction.atomic
    def create_or_update_curator_permissions(
            self,
            sub_permissions: SubPermissions,
            dto: List[CuratorPermissionsCreateDto]
    ):

        """
        Создает или обновляет права для Куратора,
        которые берет из ДТО и вяжет их на переданный объект общих прав
        """

        sub_permissions.curator_permissions.all().delete()
        for _dto in dto:
            try:
                department = Department.objects.get(pk=_dto.department_id)
            except Department.DoesNotExist:
                raise ValidationError(f"Организации с id {_dto.department_id} не существует")

            if department not in self.department_service.get_all_departments(self.permissions.department):
                raise ValidationError(f'У вас нет прав создания организации {department.name}')
            if sub_permissions.status == 'ARCHIVED':
                curator_permissions = CuratorPermissions.objects.create(
                    user_sub_permissions=sub_permissions,
                    department=department,
                    modules_permissions=_dto.modules_permissions,
                    is_active=False
                )
            else:
                if department.status == 'IS_ACTIVE':
                    curator_permissions = CuratorPermissions.objects.create(
                        user_sub_permissions=sub_permissions,
                        department=department,
                        modules_permissions=_dto.modules_permissions,
                    )
                else:
                    curator_permissions = CuratorPermissions.objects.create(
                        user_sub_permissions=sub_permissions,
                        department=department,
                        modules_permissions=_dto.modules_permissions,
                        is_active=False
                    )

            curator_permissions = self.set_modules_permissions(curator_permissions, _dto)
            sub_permissions.curator_permissions.add(curator_permissions)

    @transaction.atomic
    def create_or_update_operator_permissions(
            self,
            sub_permissions: SubPermissions,
            dto: OperatorPermissionsCreateDto
    ) -> SubPermissions.pk:

        """
        Создает или обновляет права для Оператора ЛКО,
        которые берет из ДТО и вяжет их на переданный объект общих прав
        """

        operator_permissions = sub_permissions.operator_permissions \
            if hasattr(sub_permissions, 'operator_permissions') else None

        try:
            department = Department.objects.get(pk=dto.department_id)
        except Department.DoesNotExist:
            raise ValidationError('Такой организации не существует')

        if department not in self.department_service.get_all_departments(self.permissions.department):
            raise ValidationError('У вас нет прав создания оператора в этой организации')
        if sub_permissions.status == 'ARCHIVED':
            if not operator_permissions:
                operator_permissions = OperatorLkoPermissions.objects.create(
                    user_sub_permissions=sub_permissions,
                    department=department,
                    modules_permissions=dto.modules_permissions,
                    is_active=False,
                    user=sub_permissions.user
                )
                operator_permissions.appeals_categories.set(dto.appeals_categories, clear=True)
                operator_permissions.appeals_localities.set(dto.appeals_localities, clear=True)

                operator_permissions.encouragement_categories.set(dto.encouragement_categories, clear=True)
                operator_permissions.encouragement_localities.set(dto.encouragement_localities, clear=True)

                operator_permissions.initiatives_categories.set(dto.initiative_categories + dto.initiative_subcategories, clear=True)
                operator_permissions.initiatives_municipalities.set(dto.initiative_localities, clear=True)
                operator_permissions.initiatives_localities.set(dto.initiative_localities, clear=True)

                operator_permissions.suggestion_categories.set(dto.suggestion_categories, clear=True)
                operator_permissions.suggestion_localities.set(dto.suggestion_localities, clear=True)

                operator_permissions.voting_categories.set(dto.voting_categories, clear=True)
                operator_permissions.voting_municipalities.set(dto.localities, clear=True)
                operator_permissions.voting_localities.set(dto.voting_localities, clear=True)

                operator_permissions.map_works_categories.set(dto.map_works_categories, clear=True)
                operator_permissions.map_works_municipalities.set(dto.map_works_localities, clear=True)
                operator_permissions.map_works_localities.set(dto.map_works_localities, clear=True)

                operator_permissions.plans_categories.set(dto.plans_categories, clear=True)
                operator_permissions.plans_municipalities.set(dto.plans_localities, clear=True)
                operator_permissions.plans_localities.set(dto.plans_localities, clear=True)

                operator_permissions.save()
            else:
                operator_permissions.department = department
                operator_permissions.modules_permissions = dto.modules_permissions
                operator_permissions.is_active = False
                operator_permissions.user = sub_permissions.user
                operator_permissions.appeals_categories.set(dto.appeals_categories, clear=True)
                operator_permissions.appeals_localities.set(dto.appeals_localities, clear=True)

                operator_permissions.encouragement_categories.set(dto.encouragement_categories, clear=True)
                operator_permissions.encouragement_localities.set(dto.encouragement_localities, clear=True)

                operator_permissions.initiatives_categories.set(dto.initiative_categories + dto.initiative_subcategories, clear=True)
                operator_permissions.initiatives_municipalities.set(dto.initiative_localities, clear=True)
                operator_permissions.initiatives_localities.set(dto.initiative_localities, clear=True)

                operator_permissions.suggestion_categories.set(dto.suggestion_categories, clear=True)
                operator_permissions.suggestion_localities.set(dto.suggestion_localities, clear=True)

                operator_permissions.voting_categories.set(dto.voting_categories, clear=True)
                operator_permissions.voting_municipalities.set(dto.voting_localities, clear=True)
                operator_permissions.voting_localities.set(dto.voting_localities, clear=True)

                operator_permissions.map_works_categories.set(dto.map_works_categories, clear=True)
                operator_permissions.map_works_municipalities.set(dto.map_works_localities, clear=True)
                operator_permissions.map_works_localities.set(dto.map_works_localities, clear=True)

                operator_permissions.plans_categories.set(dto.plans_categories, clear=True)
                operator_permissions.plans_municipalities.set(dto.plans_localities, clear=True)
                operator_permissions.plans_localities.set(dto.plans_localities, clear=True)

                operator_permissions.save()
        elif sub_permissions.status == 'IS_ACTIVE':
            if not operator_permissions:
                operator_permissions = OperatorLkoPermissions.objects.create(
                    user_sub_permissions=sub_permissions,
                    department=department,
                    modules_permissions=dto.modules_permissions,
                    user=sub_permissions.user,
                )

                operator_permissions.appeals_categories.set(dto.appeals_categories, clear=True)
                operator_permissions.appeals_localities.set(dto.appeals_localities, clear=True)

                operator_permissions.encouragement_categories.set(dto.encouragement_categories, clear=True)
                operator_permissions.encouragement_localities.set(dto.encouragement_localities, clear=True)

                operator_permissions.initiatives_categories.set(dto.initiative_categories + dto.initiative_subcategories, clear=True)
                operator_permissions.initiatives_municipalities.set(dto.initiative_localities, clear=True)
                operator_permissions.initiatives_localities.set(dto.initiative_localities, clear=True)

                operator_permissions.suggestion_categories.set(dto.suggestion_categories, clear=True)
                operator_permissions.suggestion_localities.set(dto.suggestion_localities, clear=True)

                operator_permissions.voting_categories.set(dto.voting_categories, clear=True)
                operator_permissions.voting_municipalities.set(dto.voting_localities, clear=True)
                operator_permissions.voting_localities.set(dto.voting_localities, clear=True)

                operator_permissions.map_works_categories.set(dto.map_works_categories, clear=True)
                operator_permissions.map_works_municipalities.set(dto.map_works_localities, clear=True)
                operator_permissions.map_works_localities.set(dto.map_works_localities, clear=True)

                operator_permissions.plans_categories.set(dto.plans_categories, clear=True)
                operator_permissions.plans_municipalities.set(dto.plans_localities, clear=True)
                operator_permissions.plans_localities.set(dto.plans_localities, clear=True)

                operator_permissions.save()

            else:
                operator_permissions.department = department
                operator_permissions.modules_permissions = dto.modules_permissions
                operator_permissions.user = sub_permissions.user
                operator_permissions.appeals_categories.set(dto.appeals_categories, clear=True)
                operator_permissions.appeals_localities.set(dto.appeals_localities, clear=True)

                operator_permissions.encouragement_categories.set(dto.encouragement_categories, clear=True)
                operator_permissions.encouragement_localities.set(dto.encouragement_localities, clear=True)

                operator_permissions.initiatives_categories.set(dto.initiative_categories + dto.initiative_subcategories, clear=True)
                operator_permissions.initiatives_municipalities.set(dto.initiative_localities, clear=True)
                operator_permissions.initiatives_localities.set(dto.initiative_localities, clear=True)

                operator_permissions.suggestion_categories.set(dto.suggestion_categories, clear=True)
                operator_permissions.suggestion_localities.set(dto.suggestion_localities, clear=True)

                operator_permissions.voting_categories.set(dto.voting_categories, clear=True)
                operator_permissions.voting_municipalities.set(dto.voting_localities, clear=True)
                operator_permissions.voting_localities.set(dto.voting_localities, clear=True)

                operator_permissions.map_works_categories.set(dto.map_works_categories, clear=True)
                operator_permissions.map_works_municipalities.set(dto.map_works_localities, clear=True)
                operator_permissions.map_works_localities.set(dto.map_works_localities, clear=True)

                operator_permissions.plans_categories.set(dto.plans_categories, clear=True)
                operator_permissions.plans_municipalities.set(dto.plans_localities, clear=True)
                operator_permissions.plans_localities.set(dto.plans_localities, clear=True)

                operator_permissions.save()

        # self.set_modules_permissions(operator_permissions, dto)

    def clear_roles_sub_permissions(self, sub_permissions: SubPermissions):

        """Отчищает объекты прав, на все роли"""

        if hasattr(sub_permissions, "admin_lko_permissions"):
            sub_permissions.admin_lko_permissions.delete()
        if hasattr(sub_permissions, "operator_permissions"):
            sub_permissions.operator_permissions.delete()

        sub_permissions.admin_lko_permissions = None
        sub_permissions.operator_permissions = None
        sub_permissions.curator_permissions.all().delete()

        sub_permissions.save()

    @transaction.atomic
    def create_or_update_sub_permissions(
            self, dto: UserSubPermissionsCreateDto,
            sub_permissions: Optional[SubPermissions] = None,
            user=None,
    ) -> SubPermissions:

        """Принимет все ролевые дополнительные права пользователя и обновляет им права"""

        if not sub_permissions:
            sub_permissions = SubPermissions.objects.create(
                email=dto.email,
                status=dto.status,
                sub_phone=dto.sub_phone,
                position=dto.position,
                user=user,
            )
        else:
            sub_permissions.email = dto.email
            sub_permissions.status = dto.status
            sub_permissions.sub_phone = dto.sub_phone
            sub_permissions.position = dto.position
            sub_permissions.user = user
            sub_permissions.save()

        self.clear_roles_sub_permissions(sub_permissions)

        if dto.admin_lko_permissions:
            self.create_or_update_admin_lko_permissions(sub_permissions=sub_permissions, dto=dto.admin_lko_permissions)

        if dto.operator_permissions:
            self.create_or_update_operator_permissions(sub_permissions=sub_permissions, dto=dto.operator_permissions)

        if dto.curator_permissions:
            self.create_or_update_curator_permissions(sub_permissions=sub_permissions, dto=dto.curator_permissions)

        return sub_permissions

    def create_or_update_department_permissions(self, department: Department, dto: DepartmentPermissionsCreateDto) \
            -> DepartmentSubPermissions:
        """Создает объект дополнительных прав организаци"""

        department_voting_permissions_service = self.department_permissions_service_factory.create(
            ModulesPermissions.VOTING,
            self.department
        )
        department_initiative_permissions_service = self.department_permissions_service_factory.create(
            ModulesPermissions.INITIATIVES,
            self.department
        )
        department_plans_permissions_service = self.department_permissions_service_factory.create(
            ModulesPermissions.PLANS,
            self.department
        )
        department_map_works_permissions_service = self.department_permissions_service_factory.create(
            ModulesPermissions.MAP_WORKS,
            self.department
        )
        department_appeals_permissions_service = self.department_permissions_service_factory.create(
            ModulesPermissions.APPEALS,
            self.department
        )
        department_encouragement_categories_service = self.department_permissions_service_factory.create(
            ModulesPermissions.ENCOURAGEMENTS,
            self.department
        )
        department_suggestion_categories_service = self.department_permissions_service_factory.create(
            ModulesPermissions.SUGGESTIONS,
            self.department
        )

        department_permissions = department.sub_permissions if hasattr(department, "sub_permissions") else None
        if not department_permissions:
            department_permissions = DepartmentSubPermissions.objects.create(
                department=department,
                modules_permissions=dto.modules_permissions
            )
        else:
            department_permissions.modules_permissions = dto.modules_permissions

        department_permissions.save(update_fields=["modules_permissions"])

        voting_categories = CoreCategory.objects.filter(pk__in=dto.voting_categories_ids) \
            if dto.voting_categories_ids else department_voting_permissions_service.get_allowed_categories()

        initiative_categories = InitiativeCategory.objects.filter(pk__in=dto.initiative_categories_ids) \
            if dto.initiative_categories_ids else department_initiative_permissions_service.get_allowed_parent_categories_pks()

        map_works_categories = WorkCategory.objects.filter(pk__in=dto.map_works_categories_ids) \
            if dto.map_works_categories_ids else department_map_works_permissions_service.get_allowed_categories()

        plans_categories = PlanCategory.objects.filter(pk__in=dto.plans_categories_ids) \
            if dto.plans_categories_ids else department_plans_permissions_service.get_allowed_categories()

        appeals_categories = Problematic.objects.filter(pk__in=dto.appeals_categories_ids) \
            if dto.appeals_categories_ids else department_appeals_permissions_service.get_allowed_categories()

        encouragement_categories = GoodsNServicesItemCategory.objects.filter(pk__in=dto.encouragement_categories_ids) \
            if dto.encouragement_categories_ids else department_encouragement_categories_service.get_allowed_categories()

        suggestion_categories = EventCategory.objects.filter(pk__in=dto.suggestion_categories_ids) \
            if dto.suggestion_categories_ids else department_suggestion_categories_service.get_allowed_categories()

        department_permissions.voting_categories.set(voting_categories)
        department_permissions.initiative_categories.set(initiative_categories)
        department_permissions.map_works_categories.set(map_works_categories)
        department_permissions.plans_categories.set(plans_categories)
        department_permissions.appeals_categories.set(appeals_categories)
        department_permissions.encouragement_categories.set(encouragement_categories)
        department_permissions.suggestion_categories.set(suggestion_categories)

        return department_permissions

    def create_or_update_department(self, serializer) -> Department:
        serializer.is_valid(raise_exception=True)
        department = serializer.save()
        return department

    @transaction.atomic
    def create_department_with_permissions(self, department_serializer,
                                           department_permissions_dto: Optional[DepartmentPermissionsCreateDto]
                                           ) -> Department:

        """Создает организацию и права для нее"""

        department = self.create_or_update_department(department_serializer)
        if department_permissions_dto:
            self.create_or_update_department_permissions(department, department_permissions_dto)
        return department

    def get_allowed_users(self):
        """Получить пользователей, доступных для редактирования текущему Администратору ЛКО"""
        allowed_departments = self.get_allowed_departments()
        operator_department_filter = \
            Q(sub_permissions__operator_permissions__department__in=allowed_departments)
        admin_department_filter = \
            Q(sub_permissions__admin_lko_permissions__department__in=allowed_departments)
        curator_department_filter = \
            Q(sub_permissions__curator_permissions__department__in=allowed_departments)

        return User.objects \
            .filter(operator_department_filter
                    | admin_department_filter
                    | curator_department_filter) \
            .exclude(pk=self.user.pk).distinct()
