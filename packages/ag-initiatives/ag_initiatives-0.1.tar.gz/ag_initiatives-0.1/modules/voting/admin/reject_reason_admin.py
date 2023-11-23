from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.voting.models import RejectReason


@admin.register(RejectReason)
class RejectReasonAdmin(TrackUserMixin, admin.ModelAdmin):
    pass
