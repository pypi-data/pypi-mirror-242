from django.contrib import admin

from modules.subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    list_display = [
        "user",
        "locality",
        "event_display",
        "module_display",
        "category_display",
        "created_at",
    ]
