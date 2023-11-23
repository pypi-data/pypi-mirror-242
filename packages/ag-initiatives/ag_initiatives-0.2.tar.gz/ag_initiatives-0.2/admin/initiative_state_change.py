from django.contrib import admin

from modules.initiatives.models import InitiativeStateChange


@admin.register(InitiativeStateChange)
class InitiativeStateChangeAdmin(admin.ModelAdmin):
    pass
