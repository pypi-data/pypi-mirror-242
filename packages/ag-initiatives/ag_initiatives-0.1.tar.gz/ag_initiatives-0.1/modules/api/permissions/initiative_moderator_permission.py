from rest_framework import permissions

from modules.core.models import User
from modules.initiatives.models import Initiative, InitiativeState


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsInitiativeModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Initiative):
        user: User = request.user
        return (
                user.is_authenticated
                and user.is_moderator
                and obj in user.moderator_initiatives_for_actions
        )


class IsModeratorAllowedToOfferChanges(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Initiative):
        user: User = request.user
        return (
                user.is_authenticated
                and user.is_moderator
                and obj.state == InitiativeState.PREMODERATION
                and obj in user.moderator_initiatives_for_actions
        )


class IsModeratorAllowedToRequestInfo(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Initiative):
        user: User = request.user
        return (
                user.is_authenticated
                and user.is_moderator
                and obj.state == InitiativeState.PREMODERATION
                and obj in user.moderator_initiatives_for_actions
        )
