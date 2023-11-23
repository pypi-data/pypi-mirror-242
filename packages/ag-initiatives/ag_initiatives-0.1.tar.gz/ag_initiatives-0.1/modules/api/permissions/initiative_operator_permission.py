from rest_framework import permissions

from modules.core.models import User
from modules.initiatives.models import Initiative
from modules.initiatives.models import InitiativeState


class IsInitiativeOperator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Initiative):
        user: User = request.user
        return (
            user.is_authenticated and user.is_operator
            and obj in user.operator_initiatives_for_actions
        )


class IsOperatorAllowedToView(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Initiative):
        user: User = request.user
        return (
            user.is_authenticated and user.is_operator
            and obj in user.operator_initiatives_for_view_access
        )


class IsOperatorAllowedToRequestInfo(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Initiative):
        user: User = request.user
        return (
            user.is_authenticated and user.is_operator
            and obj.state == InitiativeState.MODERATION
            and obj in user.operator_initiatives_for_actions
        )
