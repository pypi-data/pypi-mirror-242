from rest_framework import permissions

from modules.core.models import UserRole, User, SubPermissions, OperatorLkoPermissions


class IsAdminLKO(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_archive and UserRole.ADMIN_LKO in request.user.roles


# class IsOperatorLKO(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and UserRole.OPERATOR_LKO in request.user.roles


class IsOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_archive and UserRole.OPERATOR in request.user.roles


class IsOperatorLKOMulti(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_archive and UserRole.OPERATOR in request.user.roles \
            and User.objects.filter(pk=request.user.id).first(). \
                sub_permissions.operator_permissions.voting_municipalities.count() > 1


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and UserRole.MODERATOR in request.user.roles
        )


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and UserRole.USER in request.user.roles

# class IsOrganizer(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated and UserRole.ORGANIZER in request.user.roles
#         )
#
#
# class IsPartner(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and UserRole.PARTNER in request.user.roles
#
#
# class IsSecretary(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated and UserRole.SECRETARY in request.user.roles
#         )
#
#
# class IsCurator(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and UserRole.CURATOR in request.user.roles
