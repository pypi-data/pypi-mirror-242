from django.contrib import admin

from modules.initiatives.models import UserInitiativeApprove


@admin.register(UserInitiativeApprove)
class UserInitiativeApproveAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
