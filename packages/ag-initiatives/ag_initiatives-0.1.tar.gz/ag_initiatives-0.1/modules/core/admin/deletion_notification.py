from django.contrib import admin
from django import forms

from modules.core.mixins import TrackUserMixin
from modules.core.models import DeletionNotification


class DeletionNotificationForm(forms.ModelForm):
    class Meta:
        model = DeletionNotification
        fields = "__all__"
        widgets = {
            "header": forms.TextInput(),
        }


@admin.register(DeletionNotification)
class DeletionNotificationAdmin(TrackUserMixin, admin.ModelAdmin):
    list_display = ("header",)
    form = DeletionNotificationForm
