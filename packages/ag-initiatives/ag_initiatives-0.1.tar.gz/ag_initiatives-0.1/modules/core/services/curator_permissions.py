from abc import ABC, abstractmethod
from typing import Iterable, Any, Set, Dict, Union

from django.db.models import QuerySet

from modules.core.exceptions import LkoPermissionError
from modules.core.models import User, Locality
from modules.core.models.permissions import ModulesPermissions, CuratorPermissions
from modules.core.services import DepartmentService
from modules.core.services.locality import LocalityService
from modules.initiatives.models import Initiative
from modules.map_works.models import Works
from modules.plans.models import Plan
from modules.voting.models import Vote


class ICuratorModulePermissionService(ABC):
    """Интерфейс для работы с правами модулей от лица Куратора"""

    def __init__(self,
                 user: User,
                 locality_service: LocalityService = LocalityService(),
                 department_service: DepartmentService = DepartmentService()
                 ):
        self.user = user
        self.locality_service = locality_service
        self.department_service = department_service
        self.permissions = self.user.sub_permissions.curator_permissions

    @abstractmethod
    def get_allowed_objects(self) -> Iterable[Any]:
        pass

    @abstractmethod
    def get_allowed_categories(self):
        pass

    @abstractmethod
    def get_allowed_localities(self) -> Iterable[Locality]:
        pass


class CuratorVotingPermissionService(ICuratorModulePermissionService):
    """Реализация работы с правами с модулем Голосований от лица Куратора"""

    def get_allowed_objects(self) -> Set[Vote]:
        curator_permissions_objects = self.permissions.all()
        objects: Set[Vote] = set()
        for permission in curator_permissions_objects:
            if ModulesPermissions.VOTING not in permission.modules_permissions:
                continue

            permission_objects = Vote.objects.filter(
                locality__in=self.locality_service.get_all_localities(
                    set(permission.voting_localities.prefetch_related('localities').all()) |
                    set(permission.voting_municipalities.prefetch_related('localities').all())
                ),
                category__in=permission.voting_categories.all()

            )
            objects = objects | set(permission_objects)

        objects_ids = list(map(lambda obj: obj.pk, objects))
        return Vote.objects.filter(pk__in=objects_ids)

    def get_allowed_categories(self):
        curator_permissions_objects = self.permissions.all()
        objects: Set[Vote] = set()
        for permission in curator_permissions_objects:
            objects |= set(permission.voting_categories.all())
        return objects

    def get_allowed_localities(self) -> Iterable[Locality]:
        curator_permissions_objects = self.permissions.all()
        objects: Set[Locality] = set()
        for permission in curator_permissions_objects:
            objects |= self.locality_service.get_all_localities(
                set(permission.voting_localities.prefetch_related('localities').all()) |
                set(permission.voting_municipalities.prefetch_related('localities').all())
            )
        return objects


class CuratorPlansPermissionService(ICuratorModulePermissionService):
    """Реализация работы с правами с модулем Планов от лица Куратора"""
    def get_allowed_objects(self) -> Set[Plan]:
        curator_permissions_objects = self.permissions \
            .select_related('department') \
            .all()
        objects = set()

        for permission in curator_permissions_objects:
            if ModulesPermissions.PLANS not in permission.modules_permissions:
                continue

            permission_objects = Plan.objects.filter(
                locality__in=self.locality_service.get_all_localities(
                    set(permission.plans_localities.prefetch_related('localities').all()) |
                    set(permission.plans_municipalities.prefetch_related('localities').all())
                ),
                category__in=permission.plans_categories.all(),
                owner__in=self.department_service.get_all_departments(permission.department),
            )
            objects = objects | set(permission_objects)

        objects_ids = list(map(lambda obj: obj.pk, objects))
        return Plan.objects.filter(pk__in=objects_ids)

    def get_allowed_categories(self):
        curator_permissions_objects = self.permissions.all()
        objects = set()
        for permission in curator_permissions_objects:
            objects |= set(permission.plans_categories.all())
        return objects

    def get_allowed_localities(self) -> Iterable[Locality]:
        curator_permissions_objects = self.permissions.all()
        objects: Set[Locality] = set()
        for permission in curator_permissions_objects:
            objects |= self.locality_service.get_all_localities(
                set(permission.plans_localities.prefetch_related('localities').all()) |
                set(permission.plans_municipalities.prefetch_related('localities').all())
            )
        return objects


class CuratorInitiativePermissionService(ICuratorModulePermissionService):
    """Реализация работы с правами с модулем Инициатив от лица Куратора"""

    def get_allowed_objects(self) -> Set[Initiative]:
        curator_permissions_objects = self.permissions.all()
        objects = set()
        for permission in curator_permissions_objects:
            if ModulesPermissions.INITIATIVES not in permission.modules_permissions:
                continue

            permission_objects = Initiative.objects.filter(
                locality__in=self.locality_service.get_all_localities(
                    set(permission.initiatives_localities.prefetch_related('localities').all()) |
                    set(permission.initiatives_municipalities.prefetch_related('localities').all())
                ),
                category__in=permission.initiatives_categories.all()
            )
            objects = objects | set(permission_objects)

        objects_ids = list(map(lambda obj: obj.pk, objects))
        return Initiative.objects.filter(pk__in=objects_ids)

    def get_allowed_categories(self):
        curator_permissions_objects = self.permissions.all()
        objects = set()
        for permission in curator_permissions_objects:
            objects |= set(permission.initiatives_categories.all())
        return objects

    def get_allowed_localities(self) -> Iterable[Locality]:
        curator_permissions_objects = self.permissions.all()
        objects: Set[Locality] = set()
        for permission in curator_permissions_objects:
            objects |= self.locality_service.get_all_localities(
                set(permission.initiatives_localities.prefetch_related('localities').all()) |
                set(permission.initiatives_municipalities.prefetch_related('localities').all())
            )
        return objects


class CuratorMapWorksPermissionService(ICuratorModulePermissionService):
    """Реализация работы с правами с модулем Дорожных работ от лица Куратора"""

    def get_allowed_objects(self) -> Union[QuerySet, Works]:
        curator_permissions_objects = self.permissions \
            .select_related('department') \
            .all()
        objects = set()
        for permission in curator_permissions_objects:
            if ModulesPermissions.MAP_WORKS not in permission.modules_permissions:
                continue
            permission_objects = Works.objects.filter(
                locality__in=self.locality_service.get_all_localities(
                    set(permission.map_works_localities.prefetch_related('localities').all()) |
                    set(permission.map_works_municipalities.prefetch_related('localities').all())
                ),
                category__in=permission.map_works_categories.all(),
                owner__in=self.department_service.get_all_departments(permission.department),
            )
            objects = objects | set(permission_objects)

        objects_ids = list(map(lambda obj: obj.pk, objects))
        return Works.objects.filter(pk__in=objects_ids)

    def get_allowed_categories(self):
        curator_permissions_objects = self.permissions.all()
        objects = set()
        for permission in curator_permissions_objects:
            objects |= set(permission.map_works_categories.all())
        return objects

    def get_allowed_localities(self) -> Iterable[Locality]:
        curator_permissions_objects = self.permissions.all()
        objects: Set[Locality] = set()
        for permission in curator_permissions_objects:
            objects |= self.locality_service.get_all_localities(
                set(permission.map_works_localities.prefetch_related('localities').all()) |
                set(permission.map_works_municipalities.prefetch_related('localities').all())
            )
        return objects


class CuratorPermissionServiceFactory:
    """Фабрика, которая возвращает нужный класс в зависимости от переданного модуля"""

    SERVICE_CLASS_MAPPING: Dict[str, ICuratorModulePermissionService.__class__] = {
        ModulesPermissions.VOTING: CuratorVotingPermissionService,
        ModulesPermissions.PLANS: CuratorPlansPermissionService,
        ModulesPermissions.INITIATIVES: CuratorInitiativePermissionService,
        ModulesPermissions.MAP_WORKS: CuratorMapWorksPermissionService
    }

    def __init__(self,
                 user: User,
                 locality_service: LocalityService = LocalityService(),
                 department_service: DepartmentService = DepartmentService()
                 ):
        self.user = user
        self.locality_service = locality_service
        self.department_service = department_service

    def create(self, module: str) -> ICuratorModulePermissionService:
        service_class = self.SERVICE_CLASS_MAPPING.get(module, None)
        if not service_class:
            raise LkoPermissionError("неккоректный модуль")

        return service_class(
            user=self.user,
            locality_service=self.locality_service,
            department_service=self.department_service
        )
