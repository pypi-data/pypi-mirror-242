from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.initiatives.models import InitiativeCategory


@admin.register(InitiativeCategory)
class InitiativeCategoryAdmin(TrackUserMixin, admin.ModelAdmin):
    pass
