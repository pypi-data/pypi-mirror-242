from django.contrib import admin
from django_summernote import admin as summernote_admin
from django.db import models
from django import forms
from modules.subscriptions.models import SubscriptionTemplate


@admin.register(SubscriptionTemplate)
class SubscriptionTemplateAdmin(summernote_admin.SummernoteModelAdmin):
    summernote_fields = ["body"]
    list_display = ["title", "body"]
    formfield_overrides = {
        models.TextField: {"widget": forms.TextInput(attrs={"style": "width: 50em"})},
    }
