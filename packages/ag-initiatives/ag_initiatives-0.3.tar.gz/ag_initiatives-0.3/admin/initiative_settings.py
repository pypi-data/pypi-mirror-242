from django.contrib import admin

from modules.initiatives.models import InitiativeSettings


@admin.register(InitiativeSettings)
class InitiativeSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "user_locality_check",
    ]

    def has_delete_permission(self, request, obj=None):
        return False
