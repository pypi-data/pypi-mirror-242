from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.initiatives.models import InitiativeRejectReason


@admin.register(InitiativeRejectReason)
class InitiativeRejectReasonAdmin(TrackUserMixin, admin.ModelAdmin):
    pass
