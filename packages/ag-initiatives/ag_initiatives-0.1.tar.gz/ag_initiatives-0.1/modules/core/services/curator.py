from typing import Iterable, Union

from django.db.models import Q, QuerySet

from modules.core.exceptions import LkoPermissionError
from modules.core.models import User, Department
from modules.core.services.curator_permissions import CuratorPermissionServiceFactory
from modules.core.services.department import DepartmentListService
from modules.core.services.locality import LocalityService


class CuratorService:
    """Класс предоставляет интерфейс от лица Куратора"""

    def __init__(
        self,
        user: User,
        module: str = None,
        locality_service: LocalityService = LocalityService(),
        department_service: DepartmentListService = DepartmentListService(),
    ):
        self.user = user
        self.module = module
        self._check_default_permissions()
        self.locality_service = locality_service
        self.department_service = department_service
        self.permissions = self.user.sub_permissions.curator_permissions.all()
        self.module_permissions_service_factory = CuratorPermissionServiceFactory(user)

    def _check_default_permissions(self):
        if not self.user.is_operator:
            raise LkoPermissionError('user doesnt have role curator')
        if not hasattr(self.user, "sub_permissions") or not hasattr(self.user.sub_permissions, "curator_permissions"):
            raise LkoPermissionError('user doesnt have sub permissions')

    def get_allowed_departments(self) -> Iterable[Department]:
        main_departments = list(map(lambda permission: permission.department, self.permissions.all()))
        return self.department_service.get_all_departments(main_departments)

    def get_allowed_categories(self):
        permission_service = self.module_permissions_service_factory.create(self.module)
        return permission_service.get_allowed_categories()

    def get_allowed_localities(self):
        permission_service = self.module_permissions_service_factory.create(self.module)
        return permission_service.get_allowed_localities()

    def get_allowed_objects(self, module: str):
        permission_service = self.module_permissions_service_factory.create(module)
        return permission_service.get_allowed_objects()

    def get_allowed_users(self) -> Union[QuerySet, User]:
        """
        Получает всех пользователей, доступных этому оператору ЛКО

        Логика в том, что если организация хоть одного объекта из дополнителых прав пользователя
        находится в разрешенных данному Куратору организациях, то пользователь удовлетворяет условию
        """
        allowed_departments = self.get_allowed_departments()

        operator_department_filter = \
            Q(sub_permissions__operator_permissions__department__in=allowed_departments)
        admin_department_filter = \
            Q(sub_permissions__admin_lko_permissions__department__in=allowed_departments)
        curator_department_filter = \
            Q(sub_permissions__curator_permissions__department__in=allowed_departments)

        return User.objects\
            .filter(operator_department_filter
                    | admin_department_filter
                    | curator_department_filter)\
            .exclude(pk=self.user.pk).distinct()
