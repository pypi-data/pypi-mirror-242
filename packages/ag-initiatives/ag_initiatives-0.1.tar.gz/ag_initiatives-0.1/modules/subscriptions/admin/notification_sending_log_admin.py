from django.contrib import admin

from modules.subscriptions.models import NotificationSendingLog


@admin.register(NotificationSendingLog)
class NotificationSendingLogAdmin(admin.ModelAdmin):
    raw_id_fields = ["subscription"]
    list_display = [
        "user",
        "timestamp",
        "status",
    ]

    def user(self, instance):
        return f"{instance.subscription.user}"

    user.short_description = "Пользователь"
