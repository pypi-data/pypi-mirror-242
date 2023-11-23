from django.contrib import admin

from modules.integration.models import UserSynchronization


@admin.register(UserSynchronization)
class UserSynchronizationAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]

    class Meta:
        model = UserSynchronization
