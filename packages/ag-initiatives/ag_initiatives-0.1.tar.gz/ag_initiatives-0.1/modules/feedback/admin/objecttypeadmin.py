from django.contrib import admin
from django import forms

from modules.feedback.models import ObjectType


class ObjectTypeForm(forms.ModelForm):
    class Meta:
        model = ObjectType
        fields = "__all__"


@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    form = ObjectTypeForm
    list_display = ("id", "name")
    search_fields = (
        "id",
        "name",
    )
    list_filter = (
        # 'is_actual',
        # 'assignment_date',
    )
