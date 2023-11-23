from django.contrib import admin
from modules.core.models import Audio


@admin.register(Audio)
class AudioAdminInline(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
