from django.contrib import admin

from modules.appeals_pos.models.file import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass
