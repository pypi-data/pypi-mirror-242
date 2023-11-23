from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.map_works.models import WorkType


@admin.register(WorkType)
class WorkTypeAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = [
        "name",
    ]
