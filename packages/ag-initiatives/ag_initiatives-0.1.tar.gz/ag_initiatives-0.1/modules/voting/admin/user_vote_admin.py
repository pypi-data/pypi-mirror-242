from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.voting.models import UserVote


@admin.register(UserVote)
class UserVoteAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = [
        "esia_id",
        "vote",
        "locality",
    ]

    exclude = [
        "user",
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False

    def esia_id(self, instance):
        return instance.user.esia_id
