from django.contrib import admin

from modules.ecology.models import UserBalanceOperation


@admin.register(UserBalanceOperation)
class UserBalanceOperationAdmin(admin.ModelAdmin):
    list_display = [
        "type",
    ]

    def has_module_permission(self, request):
        return False
