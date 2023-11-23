from django.contrib import admin

from modules.voting.admin.voting_participant_admin import VotingParticipantInline
from modules.voting.models import LocalVotingGroup


@admin.register(LocalVotingGroup)
class LocalVotingGroupAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "department",
        "access_token",
        "participants_count"
    ]
    inlines = [VotingParticipantInline]
