from django.contrib import admin

from modules.appeals.models import RejectReason


@admin.register(RejectReason)
class RejectReasonAdmin(admin.ModelAdmin):
    list_display = [
        "text",
    ]
