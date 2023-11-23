from django.db.models import Q
from rest_framework import permissions

from modules.initiatives.models import Initiative
from modules.initiatives.models import (
    InitiativeOperatorCommunicationType as CommunicationType,
)
from modules.initiatives.models import InitiativeState


class IsApplicant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_simple_user


class IsInitiativeApplicant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Initiative):
        return request.user.is_authenticated and obj.user == request.user


class IsApplicantAllowedToAnswer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Initiative):
        info_requests = obj.initiative_operator_communication.filter(
            Q(
                type__in=(
                    CommunicationType.MODERATE_REQUEST,
                    CommunicationType.PREMODERATE_REQUEST,
                )
            )
            & Q(user_viewed=False)
        )
        if info_requests:
            return (
                request.user.is_authenticated
                and obj.user == request.user
                and obj.state
                in (InitiativeState.PREMODERATION, InitiativeState.MODERATION)
            )
        return False


class IsAllowedToAcceptOrRejectChanges(
    permissions.BasePermission
):  # TODO probably unnecessary to check state
    def has_object_permission(self, request, view, obj: Initiative):
        return (
            request.user.is_authenticated
            and obj.user == request.user
            and obj.state == InitiativeState.CHANGES_APPROVAL
        )
