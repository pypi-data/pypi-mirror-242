from django.contrib import admin

from modules.inventory.admin import inventory_admin_site
from modules.inventory.models import PassportSummary


# @admin.register(Passport, inventory_admin_site)
class PassportSummaryAdmin(admin.ModelAdmin):
    list_display = [
        "year",
        "generation_date",
    ]
