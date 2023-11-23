import nested_admin
from django.contrib import admin

from modules.plans.models import PlanComment


@admin.register(PlanComment)
class PlanCommentAdmin(admin.ModelAdmin):
    list_display = [
        "plan",
        "timestamp",
        "user",
        "moderated",
    ]
