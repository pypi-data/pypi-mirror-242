from django.contrib import admin

from modules.appeals.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "parent_name",
    ]

    def parent_name(self, obj: Category):
        return obj.parent.name if obj.parent else ""

    parent_name.short_description = "Родительская категория"
