from rest_framework import permissions


class CanGetSystemManuals(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_get_system_manuals"
            ).exists()
        )


class CanSinchronizeUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_sinchronize_user"
            ).exists()
        )


class CanGetEncouragements(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_get_encouragements"
            ).exists()
        )


class CanGetSuggestions(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_get_suggestions"
            ).exists()
        )


class CanGetVotes(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_get_votes"
            ).exists()
        )


class CanGetInitiatives(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_get_initiatives"
            ).exists()
        )


class CanTransmitEncouragements(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_transmit_encouragements"
            ).exists()
        )


class CanTransmitSuggestions(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_transmit_suggestions"
            ).exists()
        )


class CanGetUserBalance(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_get_user_balance"
            ).exists()
        )


class CanTransmitBonuses(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_transmit_bonuses"
            ).exists()
        )


class CanGetOperationHistoryOfUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_get_operation_history_of_user"
            ).exists()
        )

class CanTransmitCitizenCategories(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_transmit_citizen_category"
            ).exists()
        )

class CanUseEncouragements(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_use_encouragements"
            ).exists()
        )

class CanUseSuggestions(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.external_system
            and request.external_system.permission.filter(
                codename="can_use_suggestions"
            ).exists()
        )
