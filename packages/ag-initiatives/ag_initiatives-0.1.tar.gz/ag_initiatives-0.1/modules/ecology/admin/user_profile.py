from django.contrib import admin

from modules.ecology.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "state",
        "balance",
    ]

    search_fields = [
        "user__last_name",
        "user__first_name",
    ]
