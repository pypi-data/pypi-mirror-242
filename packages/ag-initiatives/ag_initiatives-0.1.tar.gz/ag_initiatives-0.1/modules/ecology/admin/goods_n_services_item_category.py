from django.contrib import admin

from modules.ecology.models import GoodsNServicesItemCategory


@admin.register(GoodsNServicesItemCategory)
class GoodsNServicesItemCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
