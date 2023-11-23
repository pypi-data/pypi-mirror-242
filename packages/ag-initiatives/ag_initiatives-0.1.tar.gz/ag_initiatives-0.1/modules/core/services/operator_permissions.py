from abc import ABC, abstractmethod
from typing import Iterable, Any, Dict, Optional

from rest_framework.exceptions import ValidationError

from modules.appeals_pos.models import Appeal
from modules.core.models import User, Department, Locality, UserRole
from modules.core.models.permissions import ModulesPermissions
from modules.core.services import DepartmentService
from modules.core.services.locality import LocalityService
from modules.ecology.models import Event, GoodsNServicesItem
from modules.feedback.models import Opinion
from modules.initiatives.models import Initiative
from modules.map_works.models import Works
from modules.plans.models import Plan
from modules.voting.models import Vote


class IOperatorLkoPermissionService(ABC):
    """Интерфейс для работы с правами модулей от лица Оператора ЛКО"""

    def __init__(self,
                 user: User,
                 locality_service: LocalityService = LocalityService(),
                 department_service: DepartmentService = DepartmentService()
                 ):
        self.user = user
        self.locality_service = locality_service
        self.department_service = department_service
        self.permissions = self.user.sub_permissions.operator_permissions

    @abstractmethod
    def get_allowed_categories(self):
        pass

    @abstractmethod
    def get_allowed_departments(self) -> Iterable[Department]:
        pass

    @abstractmethod
    def get_allowed_localities(self) -> Iterable[Locality]:
        """
        Метод получает разрешенные
        Муниципальные образования + Населенные пункты.
        """
        pass

    @abstractmethod
    def has_permissions(self, obj: Any):
        pass


class VotingOperatorLkoPermissionService(IOperatorLkoPermissionService):
    """Реализация работы с правами с модулем Голосований от лица Оператора ЛКО"""

    def get_allowed_categories(self):
        return self.permissions.voting_categories.all()

    def get_allowed_departments(self) -> Iterable[Department]:
        return self.department_service.get_all_departments(self.permissions.department)

    def get_allowed_localities(self) -> Iterable[Locality]:
        return self.locality_service.get_all_localities(set(self.permissions.voting_localities.all()))

    def has_permissions(self, obj: Vote):
        for locality in obj.locality.all():
            if locality not in self.get_allowed_localities():
                raise ValidationError("Недопустимые муниципальные образования или населенные пункты")

        if obj.category not in self.get_allowed_categories():
            raise ValidationError("Недопустимая категория")


class InitiativeOperatorLkoPermissionService(IOperatorLkoPermissionService):
    """Реализация работы с правами с модулем Инициатив от лица Оператора ЛКО"""

    def get_allowed_categories(self):
        return self.permissions.initiatives_categories.all()

    def get_allowed_departments(self) -> Iterable[Department]:
        return self.department_service.get_all_departments(self.permissions.department)

    def get_allowed_localities(self) -> Iterable[Locality]:
        return self.locality_service.get_all_localities(
            set(self.permissions.initiatives_localities.all()) |
            set(self.permissions.initiatives_municipalities.all())
        )

    def has_permissions(self, obj: Initiative):
        if obj.locality not in self.get_allowed_localities():
            raise ValidationError("Недопустимые муниципальные образования или населенные пункты")

        if obj.category not in self.get_allowed_categories():
            raise ValidationError("Недопустимая категория")


class MapWorksOperatorLkoPermissionService(IOperatorLkoPermissionService):
    """Реализация работы с правами с модулем Дорожных работ от лица Оператора ЛКО"""

    def get_allowed_categories(self):
        return self.permissions.map_works_categories.all()

    def get_allowed_departments(self) -> Iterable[Department]:
        return self.department_service.get_all_departments(self.permissions.department)

    def get_allowed_localities(self) -> Iterable[Locality]:
        return self.locality_service.get_all_localities(
            set(self.permissions.map_works_localities.all()) | set(self.permissions.map_works_municipalities.all())
        )

    def has_permissions(self, obj: Works):
        if obj.locality not in self.get_allowed_localities():
            raise ValidationError("Недопустимые муниципальные образования или населенные пункты")

        if obj.category not in self.get_allowed_categories():
            raise ValidationError("Недопустимая категория")


class PlansOperatorLkoPermissionService(IOperatorLkoPermissionService):
    """Реализация работы с правами с модулем Планов от лица Оператора ЛКО"""

    def get_allowed_categories(self):
        return self.permissions.plans_categories.all()

    def get_allowed_departments(self) -> Iterable[Department]:
        return self.department_service.get_all_departments(self.permissions.department)

    def get_allowed_localities(self) -> Iterable[Locality]:
        return self.locality_service.get_all_localities(
            set(self.permissions.plans_localities.all()) | set(self.permissions.plans_municipalities.all())
        )

    def has_permissions(self, obj: Plan):
        if obj.locality not in self.get_allowed_localities():
            raise ValidationError("Недопустимые муниципальные образования или населенные пункты")

        if obj.category not in self.get_allowed_categories():
            raise ValidationError("Недопустимая категория")


class AppealsOperatorLkoPermissionService(IOperatorLkoPermissionService):
    """Реализация работы с правами с модулем Планов от лица Оператора ЛКО"""

    def get_allowed_categories(self):
        return self.permissions.appeals_categories.all()

    def get_allowed_departments(self) -> Iterable[Department]:
        return self.department_service.get_all_departments(self.permissions.department)

    def get_allowed_localities(self) -> Iterable[Locality]:
        return self.locality_service.get_all_localities(
            set(self.permissions.appeals_localities.all())
        )

    def has_permissions(self, obj: Opinion):
        if obj.locality not in self.get_allowed_localities():
            raise ValidationError("Недопустимые муниципальные образования или населенные пункты")

        if obj.problematic not in self.get_allowed_categories():
            raise ValidationError("Недопустимая категория")


class SuggestionOperatorLkoPermissionService(IOperatorLkoPermissionService):
    """Реализация работы с правами с модулем Планов от лица Оператора ЛКО"""

    def get_allowed_categories(self):
        return self.permissions.suggestion_categories.all()

    def get_allowed_departments(self) -> Iterable[Department]:
        return self.department_service.get_all_departments(self.permissions.department)

    def get_allowed_localities(self) -> Iterable[Locality]:
        return self.locality_service.get_all_localities(
            set(self.permissions.suggestion_localities.all())
        )

    def has_permissions(self, obj: Event):
        if obj.locality not in self.get_allowed_localities():
            raise ValidationError("Недопустимые муниципальные образования или населенные пункты")

        if obj.category not in self.get_allowed_categories():
            raise ValidationError("Недопустимая категория")


class EncouragementOperatorLkoPermissionService(IOperatorLkoPermissionService):
    """Реализация работы с правами с модулем Планов от лица Оператора ЛКО"""

    def get_allowed_categories(self):
        return self.permissions.encouragement_categories.all()

    def get_allowed_departments(self) -> Iterable[Department]:
        return self.department_service.get_all_departments(self.permissions.department)

    def get_allowed_localities(self) -> Iterable[Locality]:
        return self.locality_service.get_all_localities(
            set(self.permissions.encouragement_localities.all())
        )

    def has_permissions(self, obj: GoodsNServicesItem):
        if obj.locality not in self.get_allowed_localities():
            raise ValidationError("Недопустимые муниципальные образования или населенные пункты")

        if obj.category not in self.get_allowed_categories():
            raise ValidationError("Недопустимая категория")


class OperatorLkoPermissionServiceFactory:
    """Фабрика, которая возвращает нужный класс в зависимости от переданного модуля"""

    SERVICE_CLASS_MAPPING: Dict[str, IOperatorLkoPermissionService.__class__] = {
        ModulesPermissions.VOTING: VotingOperatorLkoPermissionService,
        ModulesPermissions.INITIATIVES: InitiativeOperatorLkoPermissionService,
        ModulesPermissions.MAP_WORKS: MapWorksOperatorLkoPermissionService,
        ModulesPermissions.PLANS: PlansOperatorLkoPermissionService,
        ModulesPermissions.APPEALS: AppealsOperatorLkoPermissionService,
        ModulesPermissions.SUGGESTIONS: SuggestionOperatorLkoPermissionService,
        ModulesPermissions.ENCOURAGEMENTS: EncouragementOperatorLkoPermissionService,
    }

    def __init__(self,
                 user: User,
                 locality_service: LocalityService = LocalityService(),
                 department_service: DepartmentService = DepartmentService()
                 ):
        self.user = user
        self.locality_service = locality_service
        self.department_service = department_service

    def create(self, module: str) -> IOperatorLkoPermissionService:
        service_class = self.SERVICE_CLASS_MAPPING.get(module, None)
        if not service_class:
            raise Exception("неккоректный модуль")

        return service_class(
            user=self.user,
            locality_service=self.locality_service,
            department_service=self.department_service
        )
