from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.map_works.models import WorkReason


@admin.register(WorkReason)
class WorkReasonAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = [
        "name",
    ]
