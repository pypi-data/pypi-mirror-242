from django.contrib import admin

from modules.ecology.models import UserPurchase


@admin.register(UserPurchase)
class UserPurchaseAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "goods_n_services_item",
        "timestamp",
    ]
