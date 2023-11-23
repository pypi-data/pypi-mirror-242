import nested_admin
from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.plans.models import Plan, Location


@admin.register(Plan)
class PlanAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = [
        "name",
        "locality",
        "category",
        "publication_date",
    ]
