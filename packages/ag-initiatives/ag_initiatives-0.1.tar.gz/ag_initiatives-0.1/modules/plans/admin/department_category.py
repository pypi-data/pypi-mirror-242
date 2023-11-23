from django.contrib import admin

from modules.plans.models import DepartmentCategory


@admin.register(DepartmentCategory)
class DepartmentCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "department",
        "category",
    ]
