from django.contrib import admin
from django.db import models
from django import forms

from modules.core.mixins import TrackUserMixin
from modules.core.models import Settings
from django_summernote import admin as summernote_admin


# @admin.register(Settings)
# class SettingsAdmin(TrackUserMixin, summernote_admin.SummernoteModelAdmin):
#
#     formfield_overrides = {
#         models.TextField: {"widget": forms.TextInput(attrs={"style": "width: 50em"})},
#     }
