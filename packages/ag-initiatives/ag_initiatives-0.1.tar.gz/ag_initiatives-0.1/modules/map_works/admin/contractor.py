from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.map_works.models import Contractor


@admin.register(Contractor)
class ContractorAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = [
        "name",
    ]
