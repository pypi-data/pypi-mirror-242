from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.plans.models import Category


@admin.register(Category)
class CategoryAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = [
        "name",
    ]

    fields = [
        "name",
        "color",
        "image",
        "icon",
    ]
