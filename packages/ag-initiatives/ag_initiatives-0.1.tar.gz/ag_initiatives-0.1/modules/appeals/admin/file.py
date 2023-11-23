from django.contrib import admin

from modules.appeals.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
    ]
