from django.contrib import admin

from modules.core.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
    ]
