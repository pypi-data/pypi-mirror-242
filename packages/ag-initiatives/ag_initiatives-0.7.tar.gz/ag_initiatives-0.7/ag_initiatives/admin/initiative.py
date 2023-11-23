from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from rest_framework import serializers

from modules.core.mixins import TrackUserMixin
from modules.core.models import UserRole
from modules.initiatives.models import (
    Initiative,
    InitiativeState,
    InitiativeOperatorCommunication,
    InitiativeOperatorCommunicationType,
)

MODERATOR_STATES = [
    InitiativeState.PREMODERATION,
]

OPERATOR_STATES = [
    InitiativeState.VOTES_COLLECTION,
    InitiativeState.CONSIDERATION,
    InitiativeState.IN_PROGRESS,
    InitiativeState.ACCOMPLISHED,
]

ALL_STATES = [
    InitiativeState.PREMODERATION,
    InitiativeState.CHANGES_APPROVAL,
    InitiativeState.PREMODERATION_REJECTED,
    InitiativeState.MODERATION,
    InitiativeState.REJECTED,
    InitiativeState.VOTES_COLLECTION,
    InitiativeState.REJECTED_VOTES_THRESHOLD,
    InitiativeState.CONSIDERATION,
    InitiativeState.IN_PROGRESS,
    InitiativeState.ACCOMPLISHED,
]


BASE_FIELDS = [
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


class InitiativeOperatorCommunicationInline(admin.TabularInline):
    extra = 0
    can_delete = False
    model = InitiativeOperatorCommunication

    def get_queryset(self, request):
        return super().get_queryset(request)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Initiative)
class InitiativeAdmin(TrackUserMixin, admin.ModelAdmin):
    inlines = [InitiativeOperatorCommunicationInline]

    list_display = [
        "number",
        "creation_date_time",
        "state",
        "title",
        "locality_",
        "category",
    ]

    list_filter = [
        "state",
        "category",
    ]

    ordering = ["state", "creation_date_time", "category"]

    exclude = ["files", "type"]

    readonly_fields = [
        "files_",
    ]

    def files_(self, instance):
        html = "<ul>"
        if instance.files:
            for f in instance.files.all():
                html += f"<li><a href='{serializers.FileField().to_representation(f.file)}'>{f.name}</a></li>"
        html += "</ul>"
        return format_html(html)

    def locality_(self, instance: Initiative):
        if instance.locality.exists():
            return ', '.join(
                [locality.name for locality in instance.locality.all()])

    files_.short_description = "Список файлов"
    locality_.short_description = "Муниципальные образования"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        states = []

        if UserRole.MODERATOR in user.roles:
            states += MODERATOR_STATES

        if UserRole.OPERATOR in user.roles:
            states += OPERATOR_STATES

        if UserRole.ADMIN in user.roles:
            states += ALL_STATES

        qs = qs.filter(state__in=states)

        return qs

    def response_change(self, request, obj):
        if "_approve" in request.POST:
            self.message_user(request, "Одобрено")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
