from django import forms
from django.contrib import admin
from django.db import models
from django_summernote import admin as summernote_admin

from modules.appeals_pos.models import Settings


@admin.register(Settings)
class SettingsAdmin(summernote_admin.SummernoteModelAdmin):

    formfield_overrides = {
        models.TextField: {"widget": forms.TextInput(attrs={"style": "width: 50em"})},
    }
