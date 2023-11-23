from django.contrib import admin

from modules.initiatives.models import InitiativeFile


@admin.register(InitiativeFile)
class InitiativeFileAdmin(admin.ModelAdmin):
    pass
