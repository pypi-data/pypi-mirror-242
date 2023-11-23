from django.contrib import admin

from modules.initiatives.models import (
    InitiativeOperatorCommunication,
    InitiativeOperatorCommunicationType,
)

BASE_FIELDS = [
    "initiative",
    "user",
    "timestamp",
]

TYPE_FIELDS = {
    InitiativeOperatorCommunicationType.SYSTEM_NOTIFICATION: ["text", "files"],
    InitiativeOperatorCommunicationType.PREMODERATE_REQUEST: ["text", "files"],
    InitiativeOperatorCommunicationType.PREMODERATE_RESPONSE: ["text", "files"],
    InitiativeOperatorCommunicationType.PREMODERATE_CHANGES_REQUEST: [
        "text",
        "title",
        "description",
        "expectations",
        "files",
    ],
    InitiativeOperatorCommunicationType.PREMODERATE_CHANGES_RESPONSE: ["decision"],
    InitiativeOperatorCommunicationType.PREMODERATE_REJECT: ["text", "files"],
    InitiativeOperatorCommunicationType.MODERATE_REQUEST: ["text", "files"],
    InitiativeOperatorCommunicationType.MODERATE_RESPONSE: ["text", "files", "state"],
    InitiativeOperatorCommunicationType.MODERATE_REJECT: ["text", "files"],
    InitiativeOperatorCommunicationType.IN_PROGRESS_NOTIFICATION: ["text", "files"],
    InitiativeOperatorCommunicationType.ACCOMPLISHED_NOTIFICATION: ["text", "files"],
}


@admin.register(InitiativeOperatorCommunication)
class InitiativeOperatorCommunicationAdmin(admin.ModelAdmin):

    list_display = [
        "initiative",
        "user",
        "timestamp",
        "type",
    ]

    def get_fields(self, request, obj=None):
        if obj is None:
            return super().get_fields(request, obj)
        return BASE_FIELDS + TYPE_FIELDS[obj.type]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
