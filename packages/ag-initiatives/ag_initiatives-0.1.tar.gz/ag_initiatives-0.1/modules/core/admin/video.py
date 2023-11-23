from django.contrib import admin
from modules.core.models import Video


@admin.register(Video)
class VideoAdminInline(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
