from django.contrib import admin
from django_summernote import admin as summernote_admin
from django.db import models
from django import forms
from django.core.exceptions import ValidationError

from modules.core.mixins import TrackUserMixin
from modules.core.models import SettingsModule
from modules.core.models.settings_types import SettingsTypes


@admin.register(SettingsModule)
class SettingsModuleAdmin(TrackUserMixin, summernote_admin.SummernoteModelAdmin):
    list_display = ("header", 'type')
    summernote_fields = ["text"]
    formfield_overrides = {
        models.TextField: {"widget": forms.TextInput(attrs={"style": "width: 50em"})},
    }

    def clean_settings(self, obj):
        if obj.type == SettingsTypes.PERSONAL_DATA_USAGE_POLICY.value and SettingsModule.objects.filter(
                type=obj.type).exists():
            raise ValidationError("Блок с Политикой использования персональных данных уже создан")

    def save_model(self, request, obj, form, change):
        self.clean_settings(obj)
        super().save_model(request, obj, form, change)
