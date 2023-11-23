from django.contrib import admin

from modules.appeals_pos.models.subcategory import Subcategory


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "pos_id", "name", "category", "is_available"]
    list_filter = ["deleted"]
    fields = ["id", "pos_id", "name", "category", "is_available"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    def is_available(self, instance):
        return not instance.deleted

    is_available.boolean = True
    is_available.short_description = "Доступно"
