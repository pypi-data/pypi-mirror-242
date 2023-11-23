from django.contrib import admin

from modules.ecology.models import EventCategory


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
