from django.contrib import admin

from modules.appeals_pos.models import AppealStateChange


@admin.register(AppealStateChange)
class AppealStateChangeAdmin(admin.ModelAdmin):
    pass
