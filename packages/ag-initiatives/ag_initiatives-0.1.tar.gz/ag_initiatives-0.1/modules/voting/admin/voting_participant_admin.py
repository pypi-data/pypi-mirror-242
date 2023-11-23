from django.contrib import admin

from modules.voting.models import VotingParticipant


@admin.register(VotingParticipant)
class VotingParticipantAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "email",
    ]

    def has_module_permission(self, request):
        return False


class VotingParticipantInline(admin.TabularInline):
    verbose_name = "Участник"
    verbose_name_plural = "Участнии"
    extra = 0
    model = VotingParticipant
