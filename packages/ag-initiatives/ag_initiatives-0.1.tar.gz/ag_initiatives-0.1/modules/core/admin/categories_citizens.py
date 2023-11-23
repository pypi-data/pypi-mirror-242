from django.contrib import admin

from modules.core.models import CategoryCitizen


@admin.register(CategoryCitizen)
class CategoryCitizenAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "count_of_users",
    )
    fields = ("name",)
    ordering = ("name",)

    def count_of_users(self, obj):
        return obj.users.count()

    count_of_users.short_description = "Количество пользователей в этой категории"
