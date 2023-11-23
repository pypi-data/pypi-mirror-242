from django.contrib import admin

from modules.ecology.models import ParticipationUserEvent


@admin.register(ParticipationUserEvent)
class ParticipationUserEventAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "participant",
        "event",
        "timestamp",
    ]
