from django.contrib import admin

from modules.plans.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
    ]
