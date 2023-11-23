from typing import Dict

from rest_framework.exceptions import ValidationError

from modules.appeals_pos.models.category import Category as AppealsCategory
from modules.core.exceptions import LkoPermissionError
from modules.ecology.models import EventCategory, GoodsNServicesItemCategory
from modules.map_works.models import WorkCategory
from modules.plans.models import Category as PlanCategory
from modules.core.models import (
    User,
    Locality,
    Department,
    Category as VotingCategory
)

from modules.core.services import DepartmentService
from modules.core.services.locality import LocalityService

from modules.core.services.operator_permissions import (
    OperatorLkoPermissionServiceFactory,
    IOperatorLkoPermissionService,
)


class OperatorLkoService:
    """Класс предоставляет интерфейс от лица Оператора ЛКО"""
    def __init__(self,
                 user: User,
                 module: str, #ModulesPermissionsEnum
                 locality_service: LocalityService = LocalityService(),
                 department_service: DepartmentService = DepartmentService(),
                 permission_service_factory: OperatorLkoPermissionServiceFactory = None
                 ):
        self.user = user
        self.module = module
        self._check_default_permissions()
        self.permissions = self.user.sub_permissions.operator_permissions
        self.locality_service = locality_service
        self.department_service = department_service
        self.permission_service_factory = permission_service_factory if permission_service_factory \
            else OperatorLkoPermissionServiceFactory(user)

    def _check_default_permissions(self):
        if not self.user.is_operator:
            raise LkoPermissionError('Пользователь не имеет роли оператор ЛКО')
        if not (hasattr(self.user, 'sub_permissions') and hasattr(self.user.sub_permissions, 'operator_permissions')):
            raise LkoPermissionError('У пользователя не заданы дополнительные права для роли оператор ЛКО')

    def get_allowed_categories(self):
        permission_service = self.permission_service_factory.create(self.module)
        return permission_service.get_allowed_categories()

    def get_allowed_localities(self):
        permission_service = self.permission_service_factory.create(self.module)
        return permission_service.get_allowed_localities()

    def get_allowed_departments(self):
        permission_service = self.permission_service_factory.create(self.module)
        return permission_service.get_allowed_departments()

    def validate_departament_data(self, data: Dict, permission_service: IOperatorLkoPermissionService):
        department_id = data.get("depratment", "")
        allowed_departments = permission_service.get_allowed_departments()

        if department_id:
            department = Department.objects.filter(id=department_id).first()
            if department not in allowed_departments:
                raise ValidationError("Недопустимая организация")

    def validate_locality_data(self, data: Dict, permission_service: IOperatorLkoPermissionService):
        locality_id = data.get("locality", "")
        allowed_localities = permission_service.get_allowed_localities()

        if not hasattr(locality_id, "__iter__"):
            locality_id = [locality_id]

        if locality_id:
            locality = Locality.objects.filter(id__in=locality_id).first()
            if locality not in allowed_localities:
                raise ValidationError("Недопустимые муниципальные образования или населенные пункты")

    def validate_plan_data(self, data: Dict):
        """Проверяет входные данные по пермишену юзера(Категория Плана)"""
        permission_service = self.permission_service_factory.create(self.module)
        self.validate_locality_data(data, permission_service)

        category_id = data.get("category", "")
        allowed_categories = permission_service.get_allowed_categories()

        if not hasattr(category_id, "__iter__"):
            category_id = [category_id]
        if category_id:
            category = PlanCategory.objects.filter(id__in=category_id).first()
            if category not in allowed_categories:
                raise ValidationError("Недопустимая категория")

    def validate_voting_data(self, data: Dict):
        """Проверяет входные данные по пермишену юзера(Категория Голосований)"""
        permission_service = self.permission_service_factory.create(self.module)
        self.validate_locality_data(data, permission_service)
        self.validate_departament_data(data, permission_service)

        category_id = data.get("category", "")
        allowed_categories = permission_service.get_allowed_categories()

        if not hasattr(category_id, "__iter__"):
            category_id = [category_id]
        if category_id:
            category = VotingCategory.objects.filter(id__in=category_id).first()
            if category not in allowed_categories:
                raise ValidationError("Недопустимая категория")

    def validate_map_works_data(self, data: Dict):
        """Проверяет входные данные по пермишену юзера(Категория Ремонтные работы)"""
        permission_service = self.permission_service_factory.create(self.module)
        self.validate_locality_data(data, permission_service)

        category_id = data.get("category", "")
        allowed_categories = permission_service.get_allowed_categories()

        if not hasattr(category_id, "__iter__"):
            category_id = [category_id]
        if category_id:
            category = WorkCategory.objects.filter(id__in=category_id).first()
            if category not in allowed_categories:
                raise ValidationError("Недопустимая категория")

    def validate_appeals_data(self, data: Dict):
        """Проверяет входные данные по пермишену юзера(«Ваше мнение»)"""
        permission_service = self.permission_service_factory.create(self.module)
        self.validate_locality_data(data, permission_service)

        category_id = data.get("subcategory", "")
        allowed_categories = permission_service.get_allowed_categories()

        if not hasattr(category_id, "__iter__"):
            category_id = [category_id]
        if category_id:
            category = AppealsCategory.objects.filter(appeals__id__in=category_id)
            if not allowed_categories.filter(id__in=category).exists():
                raise ValidationError("Недопустимая категория")

    def validate_suggestion_data(self, data: Dict):
        """Проверяет входные данные по пермишену юзера(Предложений)"""
        permission_service = self.permission_service_factory.create(self.module)
        self.validate_locality_data(data, permission_service)

        category_id = data.get("category", "")
        allowed_categories = permission_service.get_allowed_categories()

        if not hasattr(category_id, "__iter__"):
            category_id = [category_id]
        if category_id:
            category = EventCategory.objects.filter(id__in=category_id).first()
            if category not in allowed_categories:
                raise ValidationError("Недопустимая категория")

    def validate_encouragement_data(self, data: Dict):
        """Проверяет входные данные по пермишену юзера(Поощрений)"""
        permission_service = self.permission_service_factory.create(self.module)
        self.validate_locality_data(data, permission_service)

        category_id = data.get("category", "")
        allowed_categories = permission_service.get_allowed_categories()

        if not hasattr(category_id, "__iter__"):
            category_id = [category_id]
        if category_id:
            category = GoodsNServicesItemCategory.objects.filter(id__in=category_id).first()
            if category not in allowed_categories:
                raise ValidationError("Недопустимая категория")