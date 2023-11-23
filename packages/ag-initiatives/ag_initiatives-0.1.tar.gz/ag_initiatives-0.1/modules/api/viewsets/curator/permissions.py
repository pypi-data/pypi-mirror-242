from rest_framework.permissions import BasePermission

from modules.core.exceptions import LkoPermissionError
from modules.core.models import UserRole
from modules.core.models.permissions import ModulesPermissions


class IsModuleCurator(BasePermission):

    def get_all_modules_permissions(self, request):
        curator_permissions = request.user.sub_permissions.curator_permissions.all()
        all_modules_permission = set()
        for permission in curator_permissions:
            all_modules_permission = all_modules_permission | set(permission.modules_permissions)

        return all_modules_permission


class IsVotingCurator(IsModuleCurator):
    def has_permission(self, request, view):
        if ModulesPermissions.VOTING not in self.get_all_modules_permissions(request):
            raise LkoPermissionError(detail="У вас нет доступа к модулю Голосования в роли Куратора")

        return request.user.is_authenticated and UserRole.CURATOR in request.user.roles


class IsMapWorksCurator(IsModuleCurator):
    def has_permission(self, request, view):
        if ModulesPermissions.MAP_WORKS not in self.get_all_modules_permissions(request):
            raise LkoPermissionError(detail="У вас нет доступа к модулю Карты в роли Куратора")

        return request.user.is_authenticated and UserRole.CURATOR in request.user.roles


class IsPlanCurator(IsModuleCurator):
    def has_permission(self, request, view):

        if ModulesPermissions.PLANS not in self.get_all_modules_permissions(request):
            raise LkoPermissionError(detail="У вас нет доступа к модулю Планы в роли Куратора")

        return request.user.is_authenticated and UserRole.CURATOR in request.user.roles



