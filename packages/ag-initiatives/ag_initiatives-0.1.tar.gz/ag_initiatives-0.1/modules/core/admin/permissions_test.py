from django.contrib import admin

from modules.core.models import OperatorLkoPermissions, SubPermissions, AdminLkoPermissions
from modules.core.models import DepartmentSubPermissions
from modules.core.models.permissions import CuratorPermissions


@admin.register(OperatorLkoPermissions)
class OperatorLkoPermissionsAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(AdminLkoPermissions)
class AdminLkoPermissionsAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


class AdminLkoPermissionsInline(admin.StackedInline):
    model = AdminLkoPermissions


class OperatorLkoPermissionsInline(admin.StackedInline):
    model = OperatorLkoPermissions


class CuratorPermissionsInline(admin.StackedInline):
    model = CuratorPermissions
    extra = 0


@admin.register(CuratorPermissions)
class CuratorPermissionsAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


# @admin.register(SubPermissions)
# class SubPermissionsAdmin(admin.ModelAdmin):
#     inlines = [AdminLkoPermissionsInline, OperatorLkoPermissionsInline]
#     exclude = ["status"]
#     search_fields = [
#         "user__first_name",
#         "user__last_name",
#         "user__patronymic_name",
#     ]
#     list_filter = []


# @admin.register(DepartmentSubPermissions)
# class DepartmentSubPermissionsAdmin(admin.ModelAdmin):
#     search_fields = [
#         "department__name",
#     ]
#
#     class Meta:
#         model = DepartmentSubPermissions
#         fields = "__all__"
