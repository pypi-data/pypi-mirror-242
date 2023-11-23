from django.contrib import admin
from django.contrib.admin import ModelAdmin

from modules.core.models import MainPageBlock


@admin.register(MainPageBlock)
class MainPageBlockAdmin(ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
