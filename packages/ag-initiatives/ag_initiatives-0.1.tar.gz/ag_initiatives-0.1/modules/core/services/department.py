from abc import ABC, abstractmethod
from typing import Dict
from typing import Iterable, Set, List, Any

from django.db.models import Q

from modules.core.models import Category as VotingCategory
from modules.core.models import Department, Locality
from modules.core.models.permissions import ModulesPermissions
from modules.core.models.permissions.department_sub_permissions import DepartmentSubPermissions
from modules.core.services.locality import LocalityService
from modules.ecology.models import EventCategory as SuggestionCategory
from modules.ecology.models import GoodsNServicesItemCategory as EncouragementCategory
from modules.feedback.models import Problematic
from modules.initiatives.models import InitiativeCategory
from modules.map_works.models import WorkCategory
from modules.plans.models import Category as PlansCategory


class DepartmentService:
    """Рекурсивно пробегается по организации и получает список ее всех ее детей"""

    @classmethod
    def get_all_departments_generator(cls, department: Department) -> Iterable[Department]:
        sub_departments = department.sub_departments.all()
        yield department
        if sub_departments:
            for _department in sub_departments:
                yield from cls.get_all_departments_generator(_department)

    @classmethod
    def get_all_departments(cls, department: Department) -> Set[Department]:
        return set(cls.get_all_departments_generator(department))

    @classmethod
    def make_list_of_departments_ids(cls, departments_set):
        return list(map(lambda department: department.pk, departments_set))

    @classmethod
    def get_sub_departments_ids(cls, department: Department):
        departments_set = cls.get_all_departments(department)
        departments_ids = cls.make_list_of_departments_ids(departments_set)
        return departments_ids

    @classmethod
    def update_status_of_sub_departments(cls, status, instance):
        if not status:
            return
        sub_departments_ids = cls.get_sub_departments_ids(instance)
        sub_departments = Department.objects.filter(~Q(status=status), pk__in=sub_departments_ids)
        sub_departments.update(status=status)

    @classmethod
    def update_queryset_status_of_sub_permissions(cls, sub_permissions_queryset, status: bool):
        sub_permissions_queryset.update(is_active=status)

    @classmethod
    def update_status_of_sub_permissions_in_sub_departments(cls, status, instance):
        sub_departments_ids = cls.get_sub_departments_ids(instance)
        sub_departments = Department.objects.filter(pk__in=sub_departments_ids)
        for sub_department in sub_departments:
            cls.update_status_of_sub_permissions(sub_department, status)

    @classmethod
    def update_status_of_sub_permissions(cls, instance: Department, status: bool):
        sub_permissions_queryset = set()
        if hasattr(instance, 'adminlkopermissions_set'):
            admin_lko_permissions_q = instance \
                .adminlkopermissions_set.filter(~Q(is_active=status))
            sub_permissions_queryset.add(admin_lko_permissions_q)
        if hasattr(instance, 'operatorlkopermissions_set'):
            operator_lko_permissions_q = instance \
                .operatorlkopermissions_set.filter(~Q(is_active=status))
            sub_permissions_queryset.add(operator_lko_permissions_q)
        if hasattr(instance, 'curatorpermissions_set'):
            curator_permissions_q = instance \
                .curatorpermissions_set.filter(~Q(is_active=status))
            sub_permissions_queryset.add(curator_permissions_q)
        for sub_permission_q in sub_permissions_queryset:
            cls.update_queryset_status_of_sub_permissions(sub_permission_q, status)


class DepartmentListService(DepartmentService):
    """Рекурсивно пробегается по организациям и получает список ее всех ее детей"""

    @classmethod
    def get_all_departments_generator(cls, departments: Iterable[Department]) -> Set[Department]:
        for department in departments:
            sub_departments = department.sub_departments.all()
            yield department
            if sub_departments:
                for _department in sub_departments:
                    yield from cls.get_all_departments_generator([_department])

    @classmethod
    def get_all_departments(cls, departments: Iterable[Department]) -> Set[Department]:
        return set(cls.get_all_departments_generator(departments))


class IDepartmentPermissionsService(ABC):

    def __init__(self,
                 department: Department,
                 locality_service: LocalityService = LocalityService(),
                 department_service: DepartmentService = DepartmentService()
                 ):
        self.department = department
        self.locality_service = locality_service
        self.department_service = department_service
        self._check_or_create_default_permissions()

    def _check_or_create_default_permissions(self):
        if hasattr(self.department, "sub_permissions"):
            return
        department_permissions = DepartmentSubPermissions.objects.create(
            department=self.department,
            modules_permissions=list(ModulesPermissions.RESOLVER.keys()),
        )
        voting_categories = VotingCategory.objects.all()
        initiative_categories = InitiativeCategory.objects.filter(parent__isnull=True)
        map_works_categories = WorkCategory.objects.all()
        plans_categories = PlansCategory.objects.all()
        appeals_categories = Problematic.objects.all()
        encouragement_categories = EncouragementCategory.objects.all()
        suggestion_categories = SuggestionCategory.objects.all()

        department_permissions.voting_categories.set(voting_categories)
        department_permissions.initiative_categories.set(initiative_categories)
        department_permissions.map_works_categories.set(map_works_categories)
        department_permissions.plans_categories.set(plans_categories)
        department_permissions.appeals_categories.set(appeals_categories)
        department_permissions.encouragement_categories.set(encouragement_categories)
        department_permissions.suggestion_categories.set(suggestion_categories)

    @abstractmethod
    def get_allowed_municipalities(self) -> List[Locality]:
        pass

    @abstractmethod
    def get_allowed_categories(self) -> List[Any]:
        pass


class VotingDepartmentPermissionsService(IDepartmentPermissionsService):

    def get_allowed_municipalities(self) -> List[Locality]:
        municipalities_with_localities = self.department.locality.all()
        municipalities = self.locality_service.filter_municipalities(municipalities_with_localities)
        return list(municipalities)

    def get_allowed_categories(self) -> List[VotingCategory]:
        return self.department.sub_permissions.voting_categories.all()


class InitiativeDepartmentPermissionsService(IDepartmentPermissionsService):

    def _get_categories_children(self, categories: Iterable[InitiativeCategory]) -> Iterable[InitiativeCategory]:
        children = InitiativeCategory.objects.filter(parent__in=categories).all()
        return children

    def get_allowed_municipalities(self) -> List[Locality]:
        municipalities_with_localities = self.department.locality.all()
        municipalities = self.locality_service.filter_municipalities(municipalities_with_localities)
        return list(municipalities)

    # TODO Нужен рефактор
    def get_allowed_parent_categories_pks(self):
        parent_categories = self.department.sub_permissions.initiative_categories \
            .filter(parent__isnull=True)

        children_categories = self.department.sub_permissions.initiative_categories.filter(
            Q(parent__isnull=False)
            & ~Q(parent__in=parent_categories)
        )

        return list(parent_categories) + list(children_categories)

    def get_allowed_categories(self) -> List[InitiativeCategory]:
        parent_categories = self.department.sub_permissions.initiative_categories \
            .filter(parent__isnull=True)
        # 🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡 #
        parents = []
        for parent in parent_categories:
            children_categories = self.department.sub_permissions.initiative_categories.filter(
                parent=parent
            )
            parents.append({
                "id": parent.id,
                "name": parent.name,
                "color": parent.color,
                "image": parent.image.url if parent.image else None,
                "children": [
                    {
                        "id": child.id,
                        "name": child.name,
                        "color": child.color,
                        "image": child.image.url if child.image else None,
                        "children": []
                    }
                    for child in children_categories
                ]
            })
        return parents


class PlansDepartmentPermissionsService(IDepartmentPermissionsService):

    def get_allowed_municipalities(self) -> List[Locality]:
        municipalities_with_localities = self.department.locality.all()
        municipalities = self.locality_service.filter_municipalities(municipalities_with_localities)
        return list(municipalities)

    def get_allowed_categories(self) -> List[Any]:
        return self.department.sub_permissions.plans_categories.all()


class MapWorksDepartmentPermissionsService(IDepartmentPermissionsService):

    def get_allowed_municipalities(self) -> List[Locality]:
        municipalities_with_localities = self.department.locality.all()
        municipalities = self.locality_service.filter_municipalities(municipalities_with_localities)
        return list(municipalities)

    def get_allowed_categories(self) -> List[Any]:
        return self.department.sub_permissions.map_works_categories.all()


class AppealsDepartmentPermissionsService(IDepartmentPermissionsService):

    def get_allowed_municipalities(self) -> List[Locality]:
        municipalities_with_localities = self.department.locality.all()
        municipalities = self.locality_service.filter_municipalities(municipalities_with_localities)
        return list(municipalities)

    def get_allowed_categories(self) -> List[Any]:
        return self.department.sub_permissions.appeals_categories.all()


class EncouragementsDepartmentPermissionsService(IDepartmentPermissionsService):

    def get_allowed_municipalities(self) -> List[Locality]:
        municipalities_with_localities = self.department.locality.all()
        municipalities = self.locality_service.filter_municipalities(municipalities_with_localities)
        return list(municipalities)

    def get_allowed_categories(self) -> List[Any]:
        return self.department.sub_permissions.encouragement_categories.all()


class SuggestionsDepartmentPermissionsService(IDepartmentPermissionsService):

    def get_allowed_municipalities(self) -> List[Locality]:
        municipalities_with_localities = self.department.locality.all()
        municipalities = self.locality_service.filter_municipalities(municipalities_with_localities)
        return list(municipalities)

    def get_allowed_categories(self) -> List[Any]:
        return self.department.sub_permissions.suggestion_categories.all()


class DepartmentPermissionsServiceFactory:
    SERVICE_CLASS_MAPPING: Dict[str, IDepartmentPermissionsService.__class__] = {
        ModulesPermissions.VOTING: VotingDepartmentPermissionsService,
        ModulesPermissions.INITIATIVES: InitiativeDepartmentPermissionsService,
        ModulesPermissions.MAP_WORKS: MapWorksDepartmentPermissionsService,
        ModulesPermissions.PLANS: PlansDepartmentPermissionsService,
        ModulesPermissions.APPEALS: AppealsDepartmentPermissionsService,
        ModulesPermissions.ENCOURAGEMENTS: EncouragementsDepartmentPermissionsService,
        ModulesPermissions.SUGGESTIONS: SuggestionsDepartmentPermissionsService,
    }

    def __init__(self,
                 locality_service: LocalityService = LocalityService(),
                 department_service: DepartmentService = DepartmentService()
                 ):
        self.locality_service = locality_service
        self.department_service = department_service

    def create(self, module: str, department: Department) -> IDepartmentPermissionsService:
        service_class = self.SERVICE_CLASS_MAPPING.get(module, None)
        if not service_class:
            raise Exception("неккоректный модуль")

        return service_class(
            department=department,
            locality_service=self.locality_service,
            department_service=self.department_service
        )
