from django.contrib import admin
from django import forms

from modules.feedback.models import Opinion


class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = "__all__"


@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "object_name",
        "email_of_responsible_person",
        "object_address",
        "placement_date",
    )
    search_fields = (
        "id",
        "user",
        "object_name",
        "email_of_responsible_person",
        "object_address",
        "text",
    )
    list_filter = (
        "object_type",
        "placement_date",
    )

    form = OpinionForm
