from django.contrib import admin
from django_summernote import admin as summernote_admin
from django.db import models
from django import forms

from modules.core.mixins import TrackUserMixin
from modules.core.models import InformationalMessages


@admin.register(InformationalMessages)
class InformationalMessagesAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = ("id", "header")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["header"].widget = forms.TextInput(attrs={"style": "width: 50em"})
        form.base_fields["text"].widget = forms.Textarea(attrs={"style": "width: 50em", "maxlength": "500"})
        return form
