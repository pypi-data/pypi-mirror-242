from rest_framework import permissions


class IsOperator(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super(IsOperator, self).has_permission(request, view)
        return is_authenticated and request.user.is_operator


# class IsOperatorLKO(permissions.IsAuthenticated):
#     def has_permission(self, request, view):
#         is_authenticated = super(IsOperatorLKO, self).has_permission(request, view)
#         return is_authenticated and request.user.is_operator_lko
#
#
# class IsCurator(permissions.IsAuthenticated):
#     def has_permission(self, request, view):
#         is_authenticated = super(IsCurator, self).has_permission(request, view)
#         return is_authenticated and request.user.is_curator
