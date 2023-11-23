from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.map_works.models import InstitutionType


@admin.register(InstitutionType)
class InstitutionTypeAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = [
        "name",
    ]
