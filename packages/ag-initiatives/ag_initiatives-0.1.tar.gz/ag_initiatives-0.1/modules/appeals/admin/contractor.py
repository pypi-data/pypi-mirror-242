from django.contrib import admin

from modules.appeals.models import Contractor


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "email",
    ]
    autocomplete_fields = ["locality"]
