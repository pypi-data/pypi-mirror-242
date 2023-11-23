from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.map_works.models import WorkCategory


@admin.register(WorkCategory)
class WorkCategoryAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = [
        "name",
    ]

    fields = [
        "name",
        "color",
        "image",
        "icon",
        "display_after_finish_days",
    ]
